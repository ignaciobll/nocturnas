import json
import requests
import sqlite3

from flask import g

DATABASE = 'db_citymapper.db'

headers = {}
bus_stops = {}
metro_stops = {}

flatten = lambda l: [item for sublist in l for item in sublist]

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
    
with open('headers.json', 'r') as fheaders:
    headers = json.load(fheaders)

def idBusStop(idStop):
    cur = get_db().cursor()
    cur.execute('SELECT id FROM bus_stops WHERE code=?',(str(idStop),))
    ans = cur.fetchone()
    return ans

def idMetroStop(idStop):
    cur = get_db().cursor()
    cur.execute('SELECT full_id FROM metro_stops WHERE id=?',(str(idStop),))
    ans = cur.fetchone()
    return ans
    
def get_stops():
    bs = get_bus_stops()
    return {"stops": [bs]}
    
def get_bus_stops():
    return {'bus_stops': [int(s) for s in bus_stops.keys()]}

def get_bus_departure(idStop):
    url = 'https://citymapper.com/api/1/departures?headways=1&ids='
    ids = bus_stops[str(idStop)]['id']
    r = requests.get(url + ids, headers=headers)
    j = json.loads(r.text)
    x = j['stops'][0]['services']
    response = {'stops': []}
    for i in range(x.__len__()):
        data = {}
        try:
            data['name'] = x[i]['route_id'].split('Bus')[-1]
        except:
            data['name'] = x[i]['route_id']
            
        data['headsign'] = x[i]['headsign']
        try:
            data['arrival'] = x[i]['live_departures_seconds'][0]
        except:
            data['arrival'] = str(x[i]['next_departures'][0])
        response['stops'].append(data)
    return response

def get_metro_departure(stop):
    url = 'https://citymapper.com/api/1/metrodepartures?headways=1&ids={}'.format(idMetroStop(stop)[0])
    print(url)
    r = requests.get(url, headers = headers)
    j = json.loads(r.text)
    ldepartures = []
    for d in j['stations'][0]['sections']:
        for departures in d['departure_groupings']:
            ldepartures.append([{"destination": j['destination_name'], "time": time(j)} for j in departures['departures']])
    return {"departures": flatten(ldepartures)}

def time(j):
    if 'time_seconds' in j.keys():        
        return j['time_seconds']
    elif 'scheduled_time' in j.keys():
        return j['scheduled_time']
    else:
        return ""
