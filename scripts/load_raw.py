import os
import duckdb
from pathlib import Path

# Répertoire de base : /opt/airflow dans Docker, racine du projet en local
BASE_DIR = Path(os.getenv("AIRFLOW_HOME", Path(__file__).parent.parent))

# Chemin vers la base DuckDB
db_path = BASE_DIR / "olist.duckdb"

# Chemin vers les CSV
data_dir = BASE_DIR / "data" / "raw"

con = duckdb.connect(str(db_path))
con.execute("CREATE SCHEMA IF NOT EXISTS raw")

csv_files = {
    "olist_orders_dataset": data_dir / "olist_orders_dataset.csv",
    "olist_customers_dataset": data_dir / "olist_customers_dataset.csv",
    "olist_order_items_dataset": data_dir / "olist_order_items_dataset.csv",
}

for table_name, csv_path in csv_files.items():
    print(f"Loading {csv_path} into raw.{table_name}...")
    con.execute(f"""
        CREATE OR REPLACE TABLE raw.{table_name} AS
        SELECT * FROM read_csv('{csv_path}', auto_detect=true)
    """)

print("Raw data loaded successfully.")
con.close()