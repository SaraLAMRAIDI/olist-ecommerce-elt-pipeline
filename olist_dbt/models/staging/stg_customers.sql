{{
    config(
        materialized='view',
        schema='staging'
    )
}}

WITH source AS (
    SELECT * FROM raw.olist_customers_dataset
),

renamed AS (
    SELECT
        customer_id,
        customer_unique_id,
        customer_zip_code_prefix AS zip_code_prefix,
        customer_city AS city,
        customer_state AS state
    FROM source
)

SELECT * FROM renamed