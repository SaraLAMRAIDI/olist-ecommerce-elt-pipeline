import duckdb
from pathlib import Path

# Connexion à la base DuckDB à la racine du projet
db_path = Path(__file__).parent.parent / "olist.duckdb"
con = duckdb.connect(str(db_path))

# Créer le schéma raw
con.execute("CREATE SCHEMA IF NOT EXISTS raw")

# Charger les 3 CSV dans le schéma raw
csv_files = {
    "olist_orders_dataset": "data/raw/olist_orders_dataset.csv",
    "olist_customers_dataset": "data/raw/olist_customers_dataset.csv",
    "olist_order_items_dataset": "data/raw/olist_order_items_dataset.csv",
}

for table_name, csv_path in csv_files.items():
    print(f"Loading {csv_path} into raw.{table_name}...")
    con.execute(f"""
        CREATE OR REPLACE TABLE raw.{table_name} AS
        SELECT * FROM read_csv('{csv_path}', auto_detect=true)
    """)

print("Raw data loaded successfully.")
con.close()