# Visualize chiffr
## Getting started
1. Clone this project
2. `pip install -r requirments.txt`
3. Place all your json files in a folder called `trips`
4. `python geoJSON.py` to preprocess the json files
5. `sh start.sh`
## Features
The home screen visualizes all routes, and assigns them a color based on the **avg speed** of that route.
![home screenshot](/screenshots/home.png?raw=true)
To view more information about a route, click on it. The new route now displays colors based on the **actual speed** of the vheicle at that point.
The top-most graphs displays the speed of the vehicle, over time. The second graphs shows the distribution of speed, according to gears. We assume that the 5 gears [1, 2, 3, 4, 5] correlate to the intervals [0-10, 10-20, 20-30, 30-40, 40-50] resspectively. If this is incorrect, since I don't know the units of measurement being used in this data, this can be easily changed.
![charts screenshot](/screenshots/charts.png?raw=true)
Hover on any point of a detailed route to get the speed at that point.
![popup screenshot](/screenshots/popup.png?raw=true)
Click on the undo button on the top left corner, to go back to all routes being displayed.
## Data Preprocessing
All data preprocessing is done in geoJSON.py
### Converting JSON to GeoJSON
The original JSON file were ~75mb combined, which is too big to serve. The JSON file is instead split into:
1. `all_lines.json`
This file represents each route as a GeoJSON line. This file represents all routes in ~25mb (although in less detail). Each line additonally contains the following:
- start_time
- end_time
- avg_speed: the average speed throughout the route
- color: interpollated from a linear gradient depending on the avg_speed
- speed_distr: Distribution (frequency) of how many times the car reported back a speed in the range [0-10, 10-20, 20-30, 30-40, 40-50, 50+]
2. Individual Points:
This file represents each route as a collection of GeoJSON Points. File sizes vary from ~2.5kb to ~250kb, but these files are only loaded as needed. On average, the web app only stores ~25mb of data at any given time. Each point additionally contains the following:
- speed
- color: interpollated from a linear gradient depending on the speed
3. `all_speeds.json`
This file stores an array for the speed represented by each line in `all_lines.json`. However, the server only returns one array at a time, as requested. This keeps the `all_lines.json` small (35mb -> 25mb) and keeps our memory consumption low. 
## Libararies used
The entire web app is written using **pure** javascript, with a few packages:
1. Mapbox GL js: I've only used this library as a render engine for maps and GeoJSON vectors.
2. Chart.js : To display native HTLM5 charts
3. Flask: to serve our web app
## Possible future work
- Add filters for dates (only see trips belonging to certain dates/times).
- Convert GeoJSON files to Mapbox vectors before serving them.