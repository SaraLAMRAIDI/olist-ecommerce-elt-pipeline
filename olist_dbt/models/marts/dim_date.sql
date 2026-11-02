{{
    config(
        materialized='table',
        schema='marts'
    )
}}

WITH date_spine AS (
    SELECT
        CAST(generated_date AS DATE) AS date_day
    FROM (
        SELECT UNNEST(
            GENERATE_SERIES(
                DATE '2016-09-01',
                DATE '2018-12-31',
                INTERVAL 1 DAY
            )
        ) AS generated_date
    )
),

final AS (
    SELECT
        date_day,
        EXTRACT(YEAR FROM date_day) AS year,
        EXTRACT(MONTH FROM date_day) AS month,
        EXTRACT(DAY FROM date_day) AS day,
        EXTRACT(DOW FROM date_day) AS day_of_week,
        CASE
            WHEN EXTRACT(DOW FROM date_day) IN (0, 6) THEN TRUE
            ELSE FALSE
        END AS is_weekend
    FROM date_spine
)

SELECT * FROM final