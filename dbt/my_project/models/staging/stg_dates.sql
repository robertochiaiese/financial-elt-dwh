{{
    config(primary_key='id')
}}

WITH dimdates AS (
    SELECT *
    FROM {{ source('raw', 'raw_dates')}}
)

SELECT
    
    REPLACE("Date"::varchar, '-', '') AS date_id,
    "Date" AS date,
    "DayLongName" AS day_long_name,
    "MonthLongName" AS month_long_name,
    "CalendarDay" AS calendar_day,
    "CalendarWeek" AS calendar_week,
    "CalendarWeekStartDateId" AS calendar_week_start_date_id,
    "CalendarWeekEndDateId" AS calendar_week_end_date_id,
    "CalendarDayInWeek" AS calendar_day_in_week,
    "CalendarMonth" AS calendar_month,
    "CalendarNumberOfDaysInMonth" AS calendar_number_of_days_in_month,
    "CalendarDayInMonth" AS calendar_day_in_month,
    "CalendarNumberOfDaysInQuarter" AS calendar_number_of_days_in_quarter,
    "CalendarYear" AS calendar_year,
    "FiscalWeek" AS fiscal_week,
    "FiscalMonth" AS fiscal_month,
    "FiscalYear" AS fiscal_year
FROM dimdates