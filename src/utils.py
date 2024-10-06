import os
import requests
import rarfile

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
