from datetime import datetime, timedelta
import json
import os
import pandas as pd
import rarfile
import requests
from retry_requests import retry
import argparse

# Function to download a file
def download_file(filename, url, data_path):
    file_path = os.path.join(data_path, filename)

    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(file_path, "wb") as f:
            f.write(response.content)
            print(f"Downloaded: {filename} successfully.")
    else:
        print(f"Failed to download: {filename}")

# Function to extract .rar files
def extract_rar(filename, data_path):
    file_path = os.path.join(data_path, filename)

    if filename.endswith(".rar"):
        with rarfile.RarFile(file_path) as rf:
            rf.extractall(data_path)
            print(f"Extracted: {filename}")

# Function to download and extract data into data folder
def download_extract(data_path, config_path):
    # Load URLs
    with open(config_path, 'r') as json_file:
        urls = json.load(json_file)

    if not os.path.exists(data_path):
        os.makedirs(data_path)

    # Download the data files
    for filename, url in urls.items():
        download_file(filename, url, data_path)

        if filename.endswith(".rar"):
            # Extract .rar
            extract_rar(filename, data_path)

if __name__ == "__main__":
    # Argument parser
    parser = argparse.ArgumentParser(description="Download and extract data.")
    parser.add_argument(
        "--data_path", 
        type=str, 
        default="../data/sathorn_surasak/raw", 
        help="Path to store downloaded data."
    )
    parser.add_argument(
        "--config_path", 
        type=str, 
        default="../config/file_urls.json", 
        help="Path to the configuration file with URLs."
    )

    args = parser.parse_args()
    
    # Call the download_extract function with the specified data and config paths
    download_extract(args.data_path, args.config_path)
