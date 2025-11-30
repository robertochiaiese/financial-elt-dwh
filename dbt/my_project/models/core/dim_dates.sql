{{
    config(primary_key='date_id')
}}

-- Base CTE: Get raw date data from staging layer
WITH base AS (
    SELECT 
         *
    FROM {{ ref('stg_dates') }}
),

-- Enhanced CTE: Add calculated fields and business logic
enhanced AS (
SELECT
    date_id,

    -- Core date components
    date::date AS date,
    calendar_year,
    calendar_month,
    calendar_day,

    -- Derived date properties for analytics
    EXTRACT(doy FROM date::date) AS day_of_year,
    EXTRACT(quarter FROM date::date) AS quarter_of_year,

    -- Formatted labels for reporting
    TO_CHAR(date::date, 'YYYY-MM') AS year_month,
    TO_CHAR(date::date, 'YYYY"Q"Q') AS year_quarter,

    -- Business flags for filtering and analysis
    CASE WHEN EXTRACT(DOW FROM date::date) IN (0, 6) THEN TRUE ELSE FALSE END AS is_weekend,
    CASE WHEN calendar_day_in_month = 1 THEN TRUE ELSE FALSE END AS is_month_start,
    CASE WHEN calendar_day_in_month = calendar_number_of_days_in_month THEN TRUE ELSE FALSE END AS is_month_end,

    -- Preserve original dimension attributes
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

-- Final select: Output enhanced date dimension
SELECT  
         * 
FROM 
         enhanced
