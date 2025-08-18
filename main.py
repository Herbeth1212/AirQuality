import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from openaq import OpenAQ
from datetime import datetime
from prophet import Prophet
import folium
import time
import os
from dotenv import load_dotenv

#loading health data
health_data = pd.read_csv("Cases_data.csv")

#loading airquality data
load_dotenv(dotenv_path=".gitignore/.env")  # this loads .env file

API_KEY = os.getenv("API_KEY")

headers = {
    "X-API-Key": API_KEY
}
headers = {
    'accept': 'application/json',
    'X-API-KEY': os.getenv("API_KEY")
}

params = {
    'date_to': '2023-12-31T23:59:59Z',
    'date_from': '2021-01-01T00:00:00Z',
    'limit': 1000,
    'page': 1,
}


# To store all results
all_data = []

while True:
    response = requests.get('https://api.openaq.org/v3/sensors/23534/days/monthly', params=params, headers=headers)

    if response.status_code != 200:
        print("Error:", response.status_code, response.text)
        break

    data = response.json()
    results = data.get("results", [])

    if not results:
        break

    all_data.extend(results)
    print(f"Fetched page {params['page']}, total records: {len(all_data)}")

    # Check if there is a next page
    meta = data.get("meta", {})
    if not meta.get("found") or (params['page'] * params['limit'] >= meta.get("found", 0)):
        break

    params["page"] += 1

# Convert to DataFrame
df = pd.DataFrame(all_data)

# Show a sample
print(df.head())

# Save to CSV
df.to_csv("delhi_pm25_2021_2023.csv", index=False)
print(f"Saved {len(df)} records to delhi_pm25_2021_2023.csv")

#data_cleaning
df['date_from'] = df['period'].apply(
    lambda d: pd.to_datetime(d['datetimeFrom']['local']).strftime("%d-%m-%y")
)
df['date_to'] = df['period'].apply(
    lambda d: pd.to_datetime(d['datetimeTo']['local']).strftime("%d-%m-%y")
)

airQuality_data = pd.read_csv("delhi_pm25_2021_2023.csv")

