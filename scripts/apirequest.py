import pandas as pd
import requests
from datetime import datetime
import os


def fetch_data():
    try:
        api_key = 'GDOKZLD88QGNA3VM'
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=IBM&apikey={api_key}&datatype=csv'

        print("Fetching the data...")
        response = requests.get(url)
        print("Data Fetched ready to be saved")

        dirpath = "/opt/airflow/data"
        os.makedirs(dirpath, exist_ok=True)

        filepath = f"/opt/airflow/data/daily_data_{datetime.today().strftime('%Y-%m-%d')}.csv"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(response.text)
            
        print("Data saved!")

        return filepath
    
    except requests.exceptions.RequestException as e:
        print(f"An occur occur: {e}")
        raise







