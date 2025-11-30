{{
    config(
        unique_key='prices_id'
    )
}}

-- Generate unique identifier and calculate key financial metrics
SELECT
    -- Surrogate key for the fact table
    ROW_NUMBER() OVER(ORDER BY date_id DESC) AS prices_id,
    
    -- Core price data from staging
    date_id,
    open_price,
    high_price,
    low_price,
    close_price,
    trading_volume,
    
    -- Daily performance metrics
    ((close_price - open_price) / open_price) * 100        AS daily_price_change_pct,
    (high_price - low_price)                               AS price_range,
    ((high_price - low_price) / open_price) * 100          AS price_range_pct,

    -- Technical indicators
    AVG(close_price) OVER (
        ORDER BY date_id
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    )  AS sma_7days,  -- 7-day simple moving average

    -- Volume analysis
    trading_volume / AVG(trading_volume) OVER (
        ORDER BY date_id
        ROWS BETWEEN 20 PRECEDING AND CURRENT ROW
    )  AS volume_ratio,  -- Volume vs 20-day average

    -- Data quality check (currently zero, might be for adjusted close in future)
    close_price - close_price                              AS adjustment_difference,

    -- Trend classification for business analysis
    CASE 
        WHEN close_price > open_price THEN 'bullish'
        WHEN close_price < open_price THEN 'bearish'
        ELSE 'neutral'
    END  AS price_trend

FROM {{ ref('stg_alpha_vantage') }}
