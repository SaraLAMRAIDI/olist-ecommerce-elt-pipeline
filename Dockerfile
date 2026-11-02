FROM apache/airflow:2.9.3

# Installer les dépendances Python nécessaires
RUN pip install --no-cache-dir \
    dbt-duckdb==1.11.1 \
    duckdb==1.5.6 \
    minio