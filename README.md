# Olist E-commerce ELT Pipeline (Local Modern Data Stack)

## 📌 Project Overview
An end-to-end ELT pipeline processing the Brazilian Olist e-commerce dataset.
Built entirely with open-source tools, running locally.

## 🏗️ Architecture
[CSV Files] → [Airflow] → [DuckDB (Raw)] → [dbt (Staging → Marts)] → [DuckDB (Analytics)]
<img width="1847" height="868" alt="Capture d&#39;écran 2026-11-02 162236" src="https://github.com/user-attachments/assets/b3972d7b-ba7d-4fb3-8f63-27b3a24e5a70" />


## 🛠️ Tech Stack
- **Orchestration:** Apache Airflow
- **Data Warehouse:** DuckDB (Serverless, in-process OLAP)
- **Transformation:** dbt Core (dbt-duckdb)
- **Data Quality:** dbt tests (unique, not_null, relationships)
- **Language:** Python, SQL

## 📂 Dataset
Olist Brazilian E-Commerce Public Dataset (9 CSV files, ~100k orders).

## 🚀 Key Features
- **Medallion Architecture:** Bronze (raw) → Silver (cleaned) → Gold (star schema).
- **Star Schema:** `fct_order_items`, `dim_customers`, `dim_products`, `dim_sellers`, `dim_date`.
- **Automated Testing:** dbt schema tests ensure data integrity.
- **Reproducible:** Runs entirely on a local machine.
