from datetime import datetime, timedelta
import openmeteo_requests
import os
import pandas as pd
import rarfile
import requests
import requests_cache
from retry_requests import retry

# path to data folder
data_path = "../data/sathorn_surasak/raw"

# Function to download a file
def download_file(filename, url):
    file_path = os.path.join(data_path, filename)

    response = requests.get(url, stream=True)

    if response.status_code == 200:
      with open(file_path, "wb") as f:
        f.write(response.content)
        print(f"Downloaded: {filename} successfully.")
    else:
      print(f"Failed to download: {file_name}")


# Function to extract .rar files
def extract_rar(filename):
  file_path = os.path.join(data_path, filename)

  if filename.endswith(".rar"):
    with rarfile.RarFile(file_path) as rf:
      rf.extractall(data_path)
      print(f"Extracted: {filename}")


# Function to download and extract data into data folder
def download_extract():
    # load urls
    with open('../config/file_urls.json', 'r') as json_file:
        urls = json.load(json_file)

    if not os.path.exists(data_path):
        os.makedirs(data_path)

    # Download the data files
    for filename, url in urls.items():
        download_file(filename, url)

        if filename.endswith(".rar"):
            # Extract .rar
            extract_rar(file_name)


# Function to get weather data for a specific date range
def fetch_weather_data(start_date, end_date, latitude, longitude):
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": end_date.strftime('%Y-%m-%d'),
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m",
            "wind_gusts_10m",
            "cloudcover"
        ]  # Relevant variables
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    hourly = response.Hourly()
    time = pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )

    weather_data = {
        "date": time,
        "temperature_2m": hourly.Variables(0).ValuesAsNumpy(),
        "relative_humidity_2m": hourly.Variables(1).ValuesAsNumpy(),
        "precipitation": hourly.Variables(2).ValuesAsNumpy(),
        "wind_speed_10m": hourly.Variables(3).ValuesAsNumpy(),
        "wind_gusts_10m": hourly.Variables(4).ValuesAsNumpy(),
        "cloudcover": hourly.Variables(5).ValuesAsNumpy()
    }

    return pd.DataFrame(data=weather_data)

def create_weather_dataset():
    # Setup caching and retry mechanisms
    cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    latitude, longitude = 13.721882, 100.530233
    start_date, end_date = datetime(2017, 12, 31), datetime(2019, 4, 1)

    # Fetch data in smaller chunks
    date_chunks = pd.date_range(start=start_date, end=end_date, freq='M')
    weather_df = pd.DataFrame()

    for i in range(len(date_chunks) - 1):
        chunk_start = date_chunks[i]
        chunk_end = date_chunks[i + 1] - timedelta(seconds=1)
        print(f"Fetching data from {chunk_start} to {chunk_end}")

        # Fetch weather data for each chunk
        chunk_data = fetch_weather_data(chunk_start, chunk_end, latitude, longitude)
        weather_df = pd.concat([weather_df, chunk_data])

    fle_path = "../data/processed/"weath
    weather_df.to_csv("../data/processed/weather.csv")

