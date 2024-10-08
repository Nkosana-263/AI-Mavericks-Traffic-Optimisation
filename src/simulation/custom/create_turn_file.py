import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime

# Load the CSV file
df = pd.read_csv("../../../data/raw/manual-volume/J4_Sathon_Surasak_volume.csv")
df["time"] = pd.to_datetime(df["time"], format="%H:%M:%S")

start = datetime.strptime("06:00:00", "%H:%M:%S")
end = datetime.strptime("09:30:00", "%H:%M:%S")

df = df[(df["time"] <= end) & (df["time"] >= start)]

# Create the root element
data = ET.Element('data')

# Create an interval element
interval = ET.SubElement(data, 'interval', id='generated', begin='0.0', end='90.0')

turn_counts = df.iloc[1:]

# Iterate through the DataFrame and create edgeRelation elements
for index, row in df.iterrows():
    if index == 0:
        continue
    
    # Define directions and their corresponding columns for turn counts
    directions = ['south', 'east', 'west', 'north']
    directions_d = ["295789573", "747478914#5", "1024938013#1", "39943703#11"]
    turn_d = {
        "295789573_L": "751479821#0",
        "295789573_R": "177961597#0",
        "747478914#5_L": "1218271275_1",
        "747478914#5_S": "1218271275",
        "1024938013#1_S": "177961597#0",
        "39943703#11_L": "177961597#0",
        "39943703#11_R": "751479821#0",
        "39943703#11_S": "1218271275"
    }
    turns = ["L", "S", "R", "U"]

    turn_counts = [row[direction] for direction in directions]
    
    for i, direction in enumerate(directions_d):
        turn = turn_d.get(f"{direction}_{turns[i]}", 0)

        if turn == 0:
            continue

        if turn_counts[i] == None:
            turn_c = str(0)
        else:
            turn_c = str(turn_counts[i])

        # Create the edgeRelation element for each turn type
        ET.SubElement(interval, 'edgeRelation',
                      attrib={
                          "from": str(direction), 
                        "to": str(turn), 
                        "count": turn_c})

# Generate the XML string
xml_str = ET.tostring(data, encoding='unicode', method='xml')

# Write to a file
with open('turn_counts.xml', 'w') as f:
    f.write(xml_str)
