"""
Financial ELT Pipeline - Airflow DAG Orchestrator

Description:
This Airflow DAG orchestrates a complete financial ELT (Extract, Load, Transform) pipeline 
that processes market data from Alpha Vantage API and dimension data into a data warehouse.

Pipeline Flow:
1. EXTRACT: 
   - Fetches daily market data from Alpha Vantage API
   - Retrieves date dimension data from local storage
   
2. LOAD:
   - Creates 'raw' schema and tables in PostgreSQL if they don't exist
   - Loads extracted data into raw tables (raw_alpha_vantage, raw_dates)
   - Performs data normalization and cleansing
   
3. TRANSFORM:
   - Executes dbt (data build tool) in Docker container
   - Transforms raw data into analytical models and data marts
   - Implements data quality checks and business logic

Key Components:
- PythonOperator for data extraction and loading tasks
- DockerOperator for dbt transformations
- PostgreSQL for data storage
- XCom for inter-task communication
- Custom Python modules for API calls and DB connections

Data Sources:
- Alpha Vantage API for real-time market data
- Local CSV file for date dimension data

Output:
- Raw data stored in PostgreSQL 'raw' schema
- Transformed data models ready for analytics and reporting
"""

from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow import DAG
from datetime import datetime, timedelta
from scripts.dbConnect import connect_to_db
import pandas as pd
from docker.types import Mount
from sqlalchemy import create_engine, schema
import logging
from sqlalchemy import Table, Column, Integer, String, MetaData, DECIMAL, Date, DateTime
from scripts.apirequest import fetch_data

# Configuration paths for dbt project and profiles
DBT_PROJECT_DIR = "C:/Users/rober/Desktop/Project-2-DW/dbt/my_project"
DBT_PROFILES_YML = "C:/Users/rober/Desktop/Project-2-DW/dbt/profiles.yml"

# Default arguments for the DAG
default_args = {
    'owner':'roberto',
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

# Database connection parameters
database = 'marketdata'
usr = 'roberto'
psw = 'password'
port = '5432'
host = 'db'

def load_to_db(ti, **kwargs):
    """
    Load extracted data into PostgreSQL database
    - Creates raw schema and tables if they don't exist
    - Loads market data and date dimension data
    - Performs data normalization on column names
    """
    print("Connecting to the database...")
    engine = connect_to_db(host, database, usr, psw, port)
    print(f"Succesfully connected to {database}")
    
    # Create raw schema and tables if they don't exist
    if not engine.dialect.has_schema(engine, "raw"):
        engine.execute(schema.CreateSchema("raw"))

        metadata = MetaData(schema="raw")

        # Define table for daily market prices
        daily_prices = Table(
            'raw_alpha_vantage', metadata,
            Column('timestamp', Date),
            Column('open', DECIMAL),
            Column('high', DECIMAL),
            Column('low', DECIMAL),
            Column('close', DECIMAL),
            Column('volume', DECIMAL),
            Column('updated_at', DateTime)
        )

        # Define table for date dimension data
        dates = Table('raw_dates', metadata,
            Column('Id', Integer, primary_key=True),
            Column('Date', Date),
            Column('DayLongName', String),
            Column('MonthLongName', String),
            Column('CalendarDay', Integer),
            Column('CalendarWeek', Integer),
            Column('CalendarWeekStartDateId', Integer, nullable=True),
            Column('CalendarWeekEndDateId', Integer, nullable=True),
            Column('CalendarDayInWeek', Integer),
            Column('CalendarMonth', Integer),
            Column('CalendarNumberOfDaysInMonth', Integer),
            Column('CalendarDayInMonth', Integer),
            Column('CalendarNumberOfDaysInQuarter', Integer),
            Column('CalendarYear', Integer),
            Column('FiscalWeek', Integer),
            Column('FiscalMonth', Integer),
            Column('FiscalYear', Integer)
        )

        metadata.create_all(engine)

        # Load date dimension data
        path_dim_data = ti.xcom_pull(key='dimdate',task_ids="extracting_daily_data")
        df_date = pd.read_csv(path_dim_data)

        print("Uploading raw_dates into raw schema")
        df_date.to_sql(
         name="raw_dates",
         con=engine,
         schema='raw',
         if_exists='replace',
         index=False
        )
        print("Done!")
    
    # Load market data
    path_market_data = ti.xcom_pull(key='marketdata',task_ids="extracting_daily_data")
    df_mk = pd.read_csv(path_market_data)

    # Normalize column names: strip, lowercase, replace spaces with underscores
    df_mk.columns = (
        df_mk.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Add update timestamp
    df_mk["updated_at"] = datetime.now()

    print("Uploading raw_alpha_vantage into raw schema")
    df_mk.to_sql(
        name="raw_alpha_vantage",
        con=engine,
        schema="raw",
        if_exists="replace",
        index=False
    )
    print("Done!")

    print("The data will be soon transformed in the datawarehouse...")

def extract_data(ti):
    """
    Extract data from various sources
    - Fetches market data from Alpha Vantage API
    - Retrieves date dimension data from local file
    - Pushes file paths to XCom for downstream tasks
    """
    print("Extracting the data...")
    PATH_MARKET_DATA = fetch_data()
    ti.xcom_push(key='marketdata', value=PATH_MARKET_DATA)
    PATH_DATES_DATA = fetch_s3_like()
    ti.xcom_push(key='dimdate', value=PATH_DATES_DATA)
    print("Data succesfully extracted!")

def fetch_s3_like():
    """Simulate fetching date dimension data from S3-like storage"""
    return '/opt/airflow/data/dimdates.csv'

# Define the DAG
with DAG(
    dag_id='etl_process_03',
    default_args=default_args,
    start_date=datetime(2025,11,16),
    catchup=False,
    description='Financial ELT Pipeline for Market Data Processing'
) as dag:
    
    # Extraction task - gets data from external sources
    extract = PythonOperator(
        task_id='extracting_daily_data',
        python_callable=extract_data
    )

    # Loading task - loads data into PostgreSQL
    load = PythonOperator(
        task_id="load_data_dwh",
        python_callable=load_to_db
    )

    # Transformation task - runs dbt models in Docker container
    transform = DockerOperator(
        task_id="transform_data",
        image='ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
        command='run',
        working_dir='/usr/app',
        mounts=[
            Mount(source=str(DBT_PROJECT_DIR),
                  target='/usr/app',
                  type='bind'),
            Mount(source=str(DBT_PROFILES_YML),
                  target='/root/.dbt/profiles.yml',
                  type='bind')
        ],
        network_mode='project-2-dw_my-network',
        docker_url=f'tcp://host.docker.internal:2375',
        auto_remove='success'
    )

# Define task dependencies
extract >> load >> transform
