from flask import Flask, render_template, send_file, jsonify
import json

app = Flask(__name__)

# load all speeds
with open('data/all_speeds.json') as speed_file:
    speeds = json.load(speed_file)

@app.route("/")
def mapbox_js():
    return render_template('mapbox_js.html')

@app.route("/data/<path>")
def send_line (path = None):
    return send_file('data/'+path, as_attachment=True)

@app.route("/data/points/<path>")
def send_point (path = None):
    return send_file('data/points/'+path, as_attachment=True)

@app.route("/data/speed/<sid>")
def send_speed (sid = None):
    if sid in speeds:
        return jsonify(speeds[sid])
    else:
        return jsonify([''])