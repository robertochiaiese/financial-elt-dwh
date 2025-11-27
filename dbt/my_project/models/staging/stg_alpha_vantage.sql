WITH stocks AS ( SELECT  
                        * 
                 FROM     
                        {{ 
                            source('raw', 'raw_alpha_vantage') 
                            }} ) 


SELECT 
    REPLACE(
    timestamp::varchar, '-', ''
    ) AS date_id,
    open AS open_price,
    high AS high_price,
    low AS low_price,
    close AS close_price,
    volume AS trading_volume,
    updated_at
FROM    
    stocks