{{
    config(primary_key='date_id')
}}


WITH base AS (
    SELECT 
         *
    FROM {{ ref('stg_dates') }}
),

enhanced AS (
SELECT
    date_id,

    date::date AS date,
    calendar_year,
    calendar_month,
    calendar_day,

    -- Derivati di utilità
    EXTRACT(doy FROM date::date) AS day_of_year,
    EXTRACT(quarter FROM date::date) AS quarter_of_year,

    -- Etichette
    TO_CHAR(date::date, 'YYYY-MM') AS year_month,
    TO_CHAR(date::date, 'YYYY"Q"Q') AS year_quarter,

    -- Flags
    CASE WHEN EXTRACT(DOW FROM date::date) IN (0, 6) THEN TRUE ELSE FALSE END AS is_weekend,
    CASE WHEN calendar_day_in_month = 1 THEN TRUE ELSE FALSE END AS is_month_start,
    CASE WHEN calendar_day_in_month = calendar_number_of_days_in_month THEN TRUE ELSE FALSE END AS is_month_end,

    -- Mantieni gli altri campi originali
    day_long_name,
    month_long_name,
    calendar_week,
    calendar_week_start_date_id,
    calendar_week_end_date_id,
    calendar_day_in_week,
    calendar_number_of_days_in_month,
    calendar_day_in_month,
    calendar_number_of_days_in_quarter,
    fiscal_week,
    fiscal_month,
    fiscal_year
FROM 
        base
)

SELECT  
         * 
FROM 
         enhanced
