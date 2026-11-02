import duckdb
import pandas as pd

# Connexion à la base DuckDB
con = duckdb.connect("olist.duckdb")

# Requête : chiffre d'affaires par État brésilien
query = """
SELECT
    customer_state,
    COUNT(*) AS orders,
    ROUND(SUM(total_item_value), 2) AS revenue
FROM main_marts.fct_order_items
GROUP BY customer_state
ORDER BY revenue DESC
LIMIT 10;
"""

# Exécution et conversion en DataFrame Pandas
df = con.sql(query).df()

# Affichage propre dans le terminal
print("\n=== Top 10 Brazilian States by Revenue ===\n")
print(df.to_string(index=False))

con.close()