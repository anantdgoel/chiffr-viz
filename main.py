from flask import Flask, render_template, send_file

app = Flask(__name__)

@app.route("/")
def mapbox_js():
    return render_template('mapbox_js.html')

@app.route("/data/<path>")
def send_line (path = None):
    return send_file('data/'+path, as_attachment=True)

@app.route("/data/points/<path>")
def send_point (path = None):
    return send_file('data/points/'+path, as_attachment=True)