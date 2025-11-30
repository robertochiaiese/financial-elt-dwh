
# Market Data Analytics Pipeline
*A fully containerized ELT pipeline for financial market data analytics.*

<img width="1170" height="621" alt="ELT process 2" src="https://github.com/user-attachments/assets/b252a2ae-be36-42fd-a514-c76a0de875e2" />


---

## Project Overview
This project implements a production-style ELT pipeline for ingesting daily stock market data from the Alpha Vantage API
, storing it in a PostgreSQL data warehouse, transforming it with dbt, orchestrating workflows via Apache Airflow, and generating interactive financial visualizations using Plotly.

It demonstrates real-world data engineering patterns:

   - Automated daily data ingestion

   - Raw → Staging → Core data modeling

   - Data quality validation

   - Reproducible analysis environment with Docker

   - Clean analytical tables for downstream BI or ML tasks

---

## Data Architecture
<img width="1132" height="540" alt="Diagramma senza titolo drawio" src="https://github.com/user-attachments/assets/b89b5375-47f0-4728-8858-d4a1bf39765f" />

This project addresses that need by transforming raw market feeds into actionable information through an automated ELT workflow. This pipeline delivers:

1. **Standardized AlphaVantage Market Data**  
   Converts raw timestamps, numeric columns, and volume data into clean, structured tables.

2. **dbt Transformations for Analytics**  
   Organizes data into staging, dimensional, and fact models optimized for financial analysis.

3. **Derived Trading & Risk Metrics**  
   - Daily price change (%)  
   - Price range and volatility indicators  
   - 7-day moving averages  
   - Volume ratios  
   - Trend classification (bullish, bearish, neutral)

4. **Interactive Visual Analysis with Plotly**  
   Automatically generates dynamic candlestick + volume charts, enabling fast interpretation of market movements.




---
## Business need

Financial analysts, traders, and individual investors often face a recurring problem: they have access to raw market data, but not to meaningful insight. 
Numbers alone don’t answer the questions that actually guide decisions:

- **Is the stock trending up or down?**
- **Was today unusually volatile?**
- **Does trading volume confirm the price movement?**
- **How does today compare to last week or last month?**

## Data Sources

### Alpha Vantage — TIME_SERIES_DAILY_ADJUSTED

   - Stock price OHLC values

   - Adjusted close

   - Trading volume

   - Timestamps

### Local Supporting Data

dimdates.csv → custom date dimension

## Project Structure
```tree
financial-elt-dwh/
├── .gitattributes
├── Dockerfile
├── README.md
├── docker-compose.yml
├── requirements.txt
├── airflow/
│   └── dags/
│       └── orchestrator.py
├── data/
│   ├── daily_data_2025-11-27.csv
│   └── dimdates.csv
├── dbt/
│   └── my_project/
│       ├── macros/
│       │   └── generate_schema_name.sql
│       └── models/
│           ├── staging/
│           │   ├── stg_alpha_vantage.sql
│           │   └── stg_dates.sql
│           ├── core/
│           │   ├── dim_dates.sql
│           │   └── fact_prices_daily.sql
│           ├── sources.yml
│           └── schema.yml
├── postgres/
│   └── airflow_setup.sql
├── scripts/
│   ├── __init__.py
│   ├── apirequest.py
│   ├── dbConnect.py
│   └── plot.py
├── tests/
│   ├── data_quality/
│   │   ├── fact_prices_tests.yml
│   │   └── raw_data_schema.yml
│   └── unit/
│       ├── test_cleaning_function.py
│       └── test_db_connection.py
└── docs/
    ├── Data_architecture.png
    ├── data_model.png
    └── data_catalog.md

```



## Example Output 


## How to Run Locally
### 1. Clone the repo
```bash
git clone https://github.com/yourusername/financial-elt-dwh.git
```
### 2. Start the environment
```bash
docker-compose up --build
```

### 3. Access components

   - Airflow UI: http://localhost:8000
   - PostgreSQL: localhost:5432
   - dbt project: /dbt/my_project


