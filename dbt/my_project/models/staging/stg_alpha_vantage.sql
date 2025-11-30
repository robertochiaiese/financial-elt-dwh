-- Source raw market data from the raw layer
WITH stocks AS ( 
    SELECT  
        * 
    FROM     
        {{ 
            source('raw', 'raw_alpha_vantage') 
        }} 
) 

-- Transform and standardize market data columns
SELECT 
    -- Create date_id by removing hyphens from timestamp (format: YYYYMMDD)
    REPLACE(
        timestamp::varchar, '-', ''
    ) AS date_id,
    
    -- Standardize price column names for clarity
    open AS open_price,
    high AS high_price,
    low AS low_price,
    close AS close_price,
    
    -- Rename volume for business context
    volume AS trading_volume,
    
    -- Keep audit timestamp for data lineage
    updated_at

FROM stocks
