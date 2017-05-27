#! /bin/python
import json,os,sqlite3

from flask import Flask
from flask import Response
from flask import jsonify
from flask import redirect

app = Flask(__name__)

import citymapperresources as cityr

@app.route('/stops/')
def get_stops():
    res = json.dumps(cityr.get_stops())
    return Response(res,mimetype="application/json")

@app.route('/stops/bus/')
def get_stop_time():
    res = json.dumps(cityr.get_bus_stops())
    return Response(res,mimetype="application/json")

@app.route('/stops/bus/<idStop>')
def get_bus_departure(idStop):
    res = json.dumps(cityr.get_bus_departure(idStop))
    return Response(res,mimetype="application/json")

@app.route('/stops/metro/<idStop>')
def get_metro_departure(idStop):
    res = json.dumps(cityr.get_metro_departure(idStop))
    return Response(response=res,mimetype="application/json")

@app.route('/ignaciobll')
def go_to_github():
    return redirect("https://www.github.com/ignaciobll")

@app.errorhandler(404)
def page_not_found(error):
    error = {"status": 404, "error": "404 resource not found"}
    res = json.dumps(error)
    return Response(response=res, status=404, mimetype="application/json")

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
