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


This project solves that need by implementing an automated ELT pipeline that turns unstructured market data into real insights.



