import sqlite3, json

conn = sqlite3.connect('db_citymapper.db')
c = conn.cursor()

bus_stops = {}

with open('stops.json', 'r') as stops_file:
    bus_stops = json.load(stops_file)

insert_bus_stop ='INSERT INTO bus_stops VALUES (?,?,?,?)'

for idStop in bus_stops:
    value = (idStop, bus_stops[idStop]['id'],bus_stops[idStop]['aliases'],bus_stops[idStop]['name'])
    c.execute(insert_bus_stop,value)

conn.commit()
conn.close()
