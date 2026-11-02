{{
    config(
        materialized='table',
        schema='marts'
    )
}}

WITH enriched AS (
    SELECT * FROM {{ ref('int_orders_enriched') }}
),

final AS (
    SELECT
        order_id,
        order_item_id,
        customer_id,
        customer_unique_id,
        product_id,
        seller_id,
        order_status,
        CAST(purchased_at AS DATE) AS purchase_date,
        customer_city,
        customer_state,
        price,
        freight_value,
        total_item_value
    FROM enriched
    WHERE order_item_id IS NOT NULL  -- on garde uniquement les lignes avec un article réel
)

SELECT * FROM final