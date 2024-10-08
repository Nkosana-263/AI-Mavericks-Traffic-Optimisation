# Traffic Optimisation and Urban Mobility - AI Mavericks

## Overview
This project is part of AI Maericks' submission for the ITU WTSA 2024 Hackathon. The proposed system leverages AI/ML models for traffic forecasting and real-time dynamic traffic signal optimisation to reduce congestion, and improve urabn mobility. By integrating data from CCTV cameras, weather APIs, and event schedules, the project aims to optimise traffic light timings, contributing to **SDG 11: sustainable cities and communities**

<p align="center">
  <img src="https://zimbabwe.iom.int/sites/g/files/tmzbdl1166/files/sdgs-icon/e_web_11.png" alt="description" width ="400" height="400">
</p>
<!-- ![](https://zimbabwe.iom.int/sites/g/files/tmzbdl1166/files/sdgs-icon/e_web_11.png) -->

## Key Features:
- **Traffic Flow Forecasting**: Generates a multi-horizon forecast of traffic volume based on past traffic data, forecasted weather and data about scheduled events.
- **Traffic Signal Optimisation**: Dynamically adjusts traffic signals to minimise congestion.

## Setup
To download data, run the following commands

```bash
python src/utils/download_data.py --data_path "data/raw" --config_path "config/file_urls.json"
 ```
and

```bash
python src/utils/download_weather_data.py --longitude 100.5214 --latitude 13.7193 --start_date 2018-01-01 --end_date 2019-01-01 --output_path "data/processed/"
```


