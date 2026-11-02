import os
import duckdb
from pathlib import Path
from minio import Minio
from minio.error import S3Error

# --- Configuration ---
# Dans Docker, le nom d'hôte est "minio" (défini dans docker-compose)
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
BUCKET_NAME = "olist-raw"

BASE_DIR = Path(os.getenv("AIRFLOW_HOME", Path(__file__).parent.parent))
DATA_DIR = BASE_DIR / "data" / "raw"
DB_PATH = BASE_DIR / "olist.duckdb"

# --- 1. Upload vers MinIO ---
client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False  # Pas de HTTPS en local
)

# Créer le bucket s'il n'existe pas
if not client.bucket_exists(BUCKET_NAME):
    client.make_bucket(BUCKET_NAME)

csv_files = [
    "olist_orders_dataset.csv",
    "olist_customers_dataset.csv",
    "olist_order_items_dataset.csv",
]

for file_name in csv_files:
    file_path = DATA_DIR / file_name
    print(f"Uploading {file_name} to MinIO...")
    client.fput_object(
        BUCKET_NAME,
        file_name,
        str(file_path),
        content_type="text/csv"
    )

# --- 2. Charger depuis MinIO vers DuckDB ---
con = duckdb.connect(str(DB_PATH))
con.execute("CREATE SCHEMA IF NOT EXISTS raw")

# Installer et charger l'extension httpfs pour lire depuis S3/MinIO
con.execute("INSTALL httpfs; LOAD httpfs;")
# Configurer la connexion S3 (MinIO)
con.execute(f"""
    SET s3_endpoint='{MINIO_ENDPOINT}';
    SET s3_access_key_id='{MINIO_ACCESS_KEY}';
    SET s3_secret_access_key='{MINIO_SECRET_KEY}';
    SET s3_use_ssl=false;
    SET s3_url_style='path';
""")

for file_name in csv_files:
    table_name = file_name.replace(".csv", "")
    # Chemin S3 vers le fichier dans MinIO
    s3_path = f"s3://{BUCKET_NAME}/{file_name}"
    print(f"Loading {s3_path} into raw.{table_name}...")
    con.execute(f"""
        CREATE OR REPLACE TABLE raw.{table_name} AS
        SELECT * FROM read_csv('{s3_path}', auto_detect=true)
    """)

print("Raw data loaded from MinIO successfully.")
con.close()