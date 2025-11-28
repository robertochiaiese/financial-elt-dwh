# Market Data Analytics Pipeline

A fully containerized data pipeline for ingesting, transforming, and analyzing
daily stock market data from Alpha Vantage(http://alphavantage.com/).  
The project uses **PostgreSQL** as the data warehouse, **dbt** for ELT
transformation, **Apache Airflow** for orchestrating, Docker for containerization and **Plotly** for interactive financial visualizations.
<img width="1170" height="621" alt="ELT process 2" src="https://github.com/user-attachments/assets/b252a2ae-be36-42fd-a514-c76a0de875e2" />


---

## Project Overview

This project builds a modular analytics pipeline capable of:

- ingesting raw market data,
- transforming it into clean analytical models using dbt,
- producing business-oriented metrics and dashboards,
- enabling reproducible financial data analysis.


---

## Data Architecture
<img width="1111" height="540" alt="data_architecture2" src="https://github.com/user-attachments/assets/356f0c87-a62c-4415-925c-ca70448c461a" />



---
## Business need

Financial analysts, traders, and individual investors often face a recurring problem: they have access to raw market data, but not to meaningful insight. 
Numbers alone don’t answer the questions that actually guide decisions:

- **Is the stock trending up or down?**
- **Was today unusually volatile?**
- **Does trading volume confirm the price movement?**
- **How does today compare to last week or last month?**

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
└── scripts/
    ├── __init__.py
    ├── apirequest.py
    ├── dbConnect.py
    └── plot.py
```




