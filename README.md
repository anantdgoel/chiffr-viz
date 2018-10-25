# Visualize chiffr
## Getting started
1. Clone this project
2. `pip install -r requirments.txt`
3. Place all your json files in a folder called `trips`
4. `python geoJSON.py` to preprocess the json files
5. `sh start.sh`
## Data Preprocessing
All data preprocessing is done in geoJSON.py
### Converting JSON to GeoJSON
The original JSON file were ~75mb combined, which is too big to serve. The JSON file is instead split into:
1. `all_lines.json`
This file is represents each route as a GeoJSON line. This file represents all routes in ~35mb (although in less detail). Each line additonally contains the following:
- start_time
- end_time
- avg_speed: the average speed throughout the route
- color: interpollated from a linear gradient depending on the avg_speed
- speed_distr: Distribution (frequency) of how many times the car reported back a speed in the range [0-10, 10-20, 20-30, 30-40, 40-50, 50+]
2. Individual Points:
This file represents each route as a collection of GeoJSON Points. File sizes vary from ~2.5kb to ~250kb, but these files are only loaded as needed. On average, the web app only stores ~36mb of data at any given time. Each point additionally contains the following:
- speed
- color: interpollated from a linear gradient depending on the speed