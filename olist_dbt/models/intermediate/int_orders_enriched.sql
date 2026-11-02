{{
    config(
        materialized='view',
        schema='intermediate'
    )
}}

WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),

order_items AS (
    SELECT * FROM {{ ref('stg_order_items') }}
),

joined AS (
    SELECT
        o.order_id,
        o.customer_id,
        c.customer_unique_id,
        c.city AS customer_city,
        c.state AS customer_state,
        o.order_status,
        o.purchased_at,
        o.approved_at,
        o.delivered_to_customer_at,
        o.estimated_delivery_at,
        oi.order_item_id,
        oi.product_id,
        oi.seller_id,
        oi.price,
        oi.freight_value,
        (oi.price + oi.freight_value) AS total_item_value
    FROM orders o
    LEFT JOIN customers c ON o.customer_id = c.customer_id
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
)

SELECT * FROM joined