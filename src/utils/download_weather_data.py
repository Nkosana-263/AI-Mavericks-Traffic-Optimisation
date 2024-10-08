from datetime import datetime, timedelta
import requests_cache
import pandas as pd
import argparse
import os

# Function to get weather data for a specific date range
def fetch_weather_data(start_date, end_date, latitude, longitude, session):
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

    response = session.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        return pd.DataFrame()  # Return an empty DataFrame on failure

    data = response.json()

    if "hourly" not in data:
        print("No hourly data in response")
        return pd.DataFrame()  # Return an empty DataFrame if data is missing

    hourly = data['hourly']
    time = pd.to_datetime(hourly['time'])

    weather_data = {
        "date": time,
        "temperature_2m": hourly["temperature_2m"],
        "relative_humidity_2m": hourly["relative_humidity_2m"],
        "precipitation": hourly["precipitation"],
        "wind_speed_10m": hourly["wind_speed_10m"],
        "wind_gusts_10m": hourly["wind_gusts_10m"],
        "cloudcover": hourly["cloudcover"]
    }

    return pd.DataFrame(data=weather_data)

# Function to create and save weather dataset
def create_weather_dataset(latitude, longitude, start_date, end_date, output_path):
    # Setup caching and retry mechanisms
    cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
    
    # Fetch data in monthly chunks
    date_chunks = pd.date_range(start=start_date, end=end_date, freq='M')
    weather_df = pd.DataFrame()

    for i in range(len(date_chunks) - 1):
        chunk_start = date_chunks[i]
        chunk_end = date_chunks[i + 1] - timedelta(seconds=1)
        print(f"Fetching data from {chunk_start} to {chunk_end}")

        # Fetch weather data for each chunk
        chunk_data = fetch_weather_data(chunk_start, chunk_end, latitude, longitude, cache_session)
        weather_df = pd.concat([weather_df, chunk_data])

    # Ensure output directory exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Save the weather data to CSV
    output_file = os.path.join(output_path, "weather.csv")
    weather_df.to_csv(output_file, index=False)
    print(f"Weather data saved to {output_file}")

if __name__ == "__main__":
    # Argument parser for dynamic inputs
    parser = argparse.ArgumentParser(description="Fetch and save weather data for a given date range and location.")
    
    parser.add_argument("--latitude", type=float, required=True, help="Latitude of the location.")
    parser.add_argument("--longitude", type=float, required=True, help="Longitude of the location.")
    parser.add_argument("--start_date", type=str, required=True, help="Start date in the format YYYY-MM-DD.")
    parser.add_argument("--end_date", type=str, required=True, help="End date in the format YYYY-MM-DD.")
    parser.add_argument("--output_path", type=str, default="../data/processed", help="Path to save the output CSV file.")
    
    args = parser.parse_args()

    # Parse the start and end dates
    start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d")

    # Call the function to create the dataset
    create_weather_dataset(args.latitude, args.longitude, start_date, end_date, args.output_path)
