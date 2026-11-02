{{
    config(
        materialized='table',
        schema='marts'
    )
}}

WITH customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),

final AS (
    SELECT
        customer_id,
        customer_unique_id,
        zip_code_prefix,
        city,
        state
    FROM customers
)

SELECT * FROM final