



# Market Data Analytics Pipeline
*A fully containerized ELT pipeline for financial market data analytics.*

<img width="1170" height="621" alt="ELT process 2" src="https://github.com/user-attachments/assets/b252a2ae-be36-42fd-a514-c76a0de875e2" />


---

## Project Overview
This project implements an ELT pipeline for ingesting daily stock market data from the Alpha Vantage API, storing it in a PostgreSQL data warehouse, transforming it with dbt, orchestrating workflows via Apache Airflow, and generating interactive financial visualizations using Plotly.

It demonstrates real-world data engineering patterns:

   - Automated daily data ingestion

   - Raw → Staging → Core data modeling

   - Data quality validation

   - Reproducible analysis environment with Docker

   - Clean analytical tables for downstream BI or ML tasks

---

## Data Architecture
<img width="1132" height="540" alt="Data_architecture" src="https://github.com/user-attachments/assets/d433c2b8-95ed-4031-bd6d-8043dfe22835" />


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
   Generates dynamic candlestick + volume charts, enabling fast interpretation of market movements.



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


## Data Warehouse Layers

### Raw Layer (Bronze)

Contains raw CSV/API data with no transformations.

| Attribute       | Details                                         |
|-----------------|------------------------------------------------|
| **Object Type** | Tables                                         |
| **Transformations** | None                                       |
| **Purpose**     | Preserve source-of-truth data exactly as delivered |
| **Tables**      | `raw.raw_alpha_vantage` <br> `raw.raw_dates`   |

---

###  Staging Layer (Silver)

Standardizes formats and enforces consistency.

| Attribute       | Details                                         |
|-----------------|------------------------------------------------|
| **Object Type** | Tables                                         |
| **Transformations Include** | - Type casting (numeric, timestamps) <br> - Column renaming <br> - Alignment to analysis-ready format  <br> - Cleaning source inconsistencies <br> - Normalization of structure <br>  |
| **dbt Models**  | `stg_alpha_vantage.sql` <br> `stg_dates.sql`  |

---

###  Core Layer (Gold)

Business-ready models for analytics.

| Attribute       | Details                                         |
|-----------------|------------------------------------------------|
| **Object Type** | Views & Tables                                 |
| **Transformations Include** | - Daily price metrics <br> - % price change <br> - Volatility indicators <br> - Moving averages <br> - Trend classification (bullish, bearish, neutral) |
| **dbt Models**  | `fact_prices_daily.sql` <br> `dim_dates.sql`  |



## Example Output 
<div align="center">
<img width="812" height="203" alt="image" src="https://github.com/user-attachments/assets/c10fba3b-767b-481b-bd8e-a3800c1821f1" />
</div>


<img width="1208" height="444" alt="newplot (1)" src="https://github.com/user-attachments/assets/07360bb7-fb54-4209-9089-71f566aae179" />
scripts/plot.py
```
  --- STOCK ANALYSIS REPORT ---

    The stock is trending UP.
    Today’s volatility is within normal range.
    Volume does not strongly confirm today's price action.

    --- Comparison ---
    Close today: 308.58
    7-day avg: 302.03
    30-day avg: 274.08
```


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


## How to Run Locally
### 1. Clone the repo
```bash
git clone https://github.com/robertochiaiese/financial-elt-dwh.git
```
### 2. Start the environment
```bash
docker-compose up --build
```

### 3. Access components

   - Airflow UI: http://localhost:8000
   - PostgreSQL: localhost:5432
   - dbt project: /dbt/my_project



##  Technology Stack

| Layer | Technologies |
|-------|-------------|
| **Orchestration** | ![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white) |
| **Data Processing** | ![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white) ![Pandas](https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white) |
| **Database** | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white) |
| **Containerization** | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) |
| **Visualization** | ![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white) |
| **Language** | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) |

##  Contact

**Roberto Chiaiese**  


LinkedIn: *[Roberto Chiaiese](https://www.linkedin.com/in/roberto-chiaiese-7b90b8248/)*
