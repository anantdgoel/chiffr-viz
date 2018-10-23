from tqdm import tqdm
import json
from enum import Enum
from os import listdir
from os.path import isfile, join
import random
import string

# Global vars / Ideally would be in a config file but that's clutter for a take-home project
INPUT_FOLDER = './trips/'
COLOR_A = (21, 101, 192)
COLOR_B = (185, 43, 39)

# Enum represenation of RGB to reduce errors where the wrong color field is accessed (helps when coding at 4am)
class Color(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2

def explore(files):
    ''' return the max and min speed found in our dataset '''
    speed_list = []
    for json_file in files:
        with open(json_file) as json_fd:
            json_data = json.load(json_fd)
            for coords in json_data['coords']:
                speed_list.append(coords['speed'])
    
    min_speed = min(speed_list)
    max_speed = max(speed_list)

    return (max_speed, min_speed)

def normalize(max_val, min_val, target_val):
    ''' given a value, return a normalized value i.e. between 0 and 1 '''
    return (target_val-min_val)/(max_val-min_val)

def interpolate(x, color):
    ''' given a x%, return a color x% between COLOR_A and COLOR_B '''
    return COLOR_A[color.value] + x * (COLOR_B[color.value] - COLOR_A[color.value])

def speed_to_gradient(max_speed, min_speed, target_speed):
    ''' given a speed, return a color that can used to represent that speed '''
    target_speed = normalize(max_speed, min_speed, target_speed)
    rgb = (interpolate(target_speed, Color.RED), interpolate(target_speed, Color.GREEN), interpolate(target_speed, Color.BLUE))
    return rgb_to_hex(rgb)

def rgb_to_hex(rgb):
    ''' convert rgb values to hex color for the web '''
    return "#{0:02x}{1:02x}{2:02x}".format(safe_hex(rgb[Color.RED.value]), safe_hex(rgb[Color.GREEN.value]), safe_hex(rgb[Color.BLUE.value]))

def safe_hex(x):
    ''' ensure x is between 0 and 255 to ensure safe hex conversions '''
    return int(round(max(0, min(x, 255))))

def line_to_point(geojson_line, max_speed, min_speed):
    ''' given a GeoJSON line, return a collection of GeoJSON points ''' 
    point_collection = {
        'type': 'FeatureCollection',
        'features': [] 
    }

    color = [speed_to_gradient(max_speed, min_speed, speed) for speed in geojson_line['properties']['speed']]

    for idx, coords in enumerate(geojson_line['geometry']['coordinates']):
        point = {
            'type': 'Feature',
            'properties': {
                'speed': geojson_line['properties']['speed'][idx],
                'color': color[idx]
            },
            'geometry': {
                'type': 'Point',
                'coordinates': coords
            }
        }
        point_collection['features'].append(point)
    
    return point_collection


def json_to_geojson(json_fd, max_speed, min_speed):
    ''' given a json file as defined by comma ai, return a GeoJSON line '''
    json_data = json.load(json_fd)
    geo_json = {
        'type': 'Feature',
        'properties': {
            'start_time': "",
            'end_time': "",
            'avg_speed': "",
            'color': "",
            'speed_distr': [0, 0, 0, 0, 0, 0], # represents chart bins in format [0-10, 10-20, 20-30, 30-40, 40-50, 50+]
            'speed': []
        },
        'geometry': {
            'type': 'LineString',
            'coordinates': []
        }
    }
    geo_json['properties']['start_time'] = json_data['start_time']
    geo_json['properties']['end_time'] = json_data['end_time']
    for coords in json_data['coords']:
        geo_json['geometry']['coordinates'].append([coords['lng'], coords['lat']])
        geo_json['properties']['speed'].append(coords['speed'])
        geo_json['properties']['speed_distr'][int(coords['speed']/10)] += 1
    avg_speed = sum(geo_json['properties']['speed'])/len(geo_json['properties']['speed'])
    geo_json['properties']['avg_speed'] = round(avg_speed, 2)
    geo_json['properties']['color'] = speed_to_gradient(max_speed, min_speed, avg_speed)
    return geo_json

def write_json(json_data, filename):
    ''' given some json_data and the name of a file, write that data to that file '''
    with open(filename, 'w') as outfile:
        json.dump(json_data, outfile)

def main():
    # get a list of all files in INPUT_FOLDER
    files = [join(INPUT_FOLDER, f) for f in listdir(INPUT_FOLDER) if isfile(join(INPUT_FOLDER, f))]

    # get max and min speed found in our data
    max_speed, min_speed = explore(files)

    geo_json = {
        'type': 'FeatureCollection',
        'features': []
    }
    
    # iterate through all json files to get GeoJSON data
    for json_file in tqdm(files):
        with open(json_file) as json_fd:
            # generate line represenation from json
            line = json_to_geojson(json_fd, max_speed, min_speed)

            # generate random urls for the webapp to query the point data from
            points_url = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(5))
            points_url = 'points/' + points_url + '.json'

            # Map points to lines
            line['properties']['points_url'] = points_url

            # Add line to our collection
            geo_json['features'].append(line)

            # generate the point representation of line and write to file
            point_collection = line_to_point(line, max_speed, min_speed)
            write_json(point_collection, points_url)
        
    for line in geo_json['features']:
        del line['properties']['speed']

    # write out our GeoJSON for lines
    write_json(geo_json, 'all_lines.json')

if __name__ == '__main__':
    main() 
