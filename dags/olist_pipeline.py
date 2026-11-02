from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='olist_elt_pipeline',
    default_args=default_args,
    description='End-to-end ELT pipeline for Olist e-commerce data',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['olist', 'elt', 'dbt'],
) as dag:

    load_raw_data = BashOperator(
        task_id='load_raw_data',
        bash_command='python /opt/airflow/scripts/load_raw.py',
    )

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/airflow/olist_dbt && dbt run --profiles-dir /opt/airflow/olist_dbt',
    )

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='cd /opt/airflow/olist_dbt && dbt test --profiles-dir /opt/airflow/olist_dbt',
    )

    load_raw_data >> dbt_run >> dbt_test