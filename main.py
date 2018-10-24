from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, json, send_from_directory, send_file
from flask_cors import CORS
import os

app = Flask(__name__)
app.config.from_envvar('APP_CONFIG_FILE', silent=True)
CORS(app)
MAPBOX_ACCESS_KEY = app.config['MAPBOX_ACCESS_KEY']

@app.route("/")
def mapbox_js():
    return render_template(
        'mapbox_js.html',
        ACCESS_KEY=MAPBOX_ACCESS_KEY
    )

@app.route("/data/<path>")
def send_line (path = None):
    return send_file(path, as_attachment=True)

@app.route("/data/points/<path>")
def send_point (path = None):
    return send_file('points/'+path, as_attachment=True)