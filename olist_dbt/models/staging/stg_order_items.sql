{{
    config(
        materialized='view',
        schema='staging'
    )
}}

WITH source AS (
    SELECT * FROM raw.olist_order_items_dataset
),

renamed AS (
    SELECT
        order_id,
        order_item_id,
        product_id,
        seller_id,
        CAST(shipping_limit_date AS TIMESTAMP) AS shipping_limit_at,
        CAST(price AS DOUBLE) AS price,
        CAST(freight_value AS DOUBLE) AS freight_value
    FROM source
)

SELECT * FROM renamed