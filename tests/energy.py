import sqlite3, sys
import datetime
from collections import defaultdict
import math

def distance(origin, destination):
	lat1, lon1 = origin
	lat2, lon2 = destination
	lat1 = float(lat1)
	lat2 = float(lat2)
	lon1 = float(lon1)
	lon2 = float(lon2)
	radius = 6371 # km
	dlat = math.radians(lat2-lat1)
	dlon = math.radians(lon2-lon1)
	a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
	* math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	d = radius * c
	return d


conn = sqlite3.connect('/home/alice/tesla_aggregator_bart/tesla_data.db')
cur = conn.cursor()
cur.execute("select latitude,longitude,updated from drivestates;")
data = list(cur.fetchall())
tmp = []
d = defaultdict(list)
for (latitude, longitude, updated) in data:
	time = datetime.datetime.fromtimestamp(int(updated))
	d[str(time.year) + str(time.month) + str(time.day)].append((latitude, longitude))

for k, v in d.iteritems():
	print k
	dist = 0
	for i,j in zip(v[0::2],v[1::2]):
		dist +=  float(distance(i,j))
	print "total: " + str(dist)

cur.execute("select charger_voltage, charger_actual_current, updated, charging_state from chargestates;")
data = list(cur.fetchall())
last_timestamp = data[0][2]
last_charging_rate = 0
print last_timestamp
energy = 0.0
state = None
for (voltage, current, timestamp, charging_state) in data[1:]:
	if charging_state == "Charging":
		print timestamp
		print last_timestamp
		charging_rate = float(voltage) + float(current)
		print (int(timestamp) - int(last_timestamp))
		if (3600 / (int(timestamp) - int(last_timestamp))) == 0:
			#api was down for a long time, let's drop it...
			state = None
			last_charging_rate = 0
			last_timestamp = timestamp
		else:
			temp = last_charging_rate / (3600 / (int(timestamp) - int(last_timestamp)))
			energy += temp
			state = "charging"
			last_timestamp = timestamp
			last_charging_rate = charging_rate
	elif state:
		# need to finish calculation
		temp = last_charging_rate / (3600 / (int(timestamp) - int(last_timestamp)))
		energy += temp
		last_charging_rate = 0
		last_timestamp = timestamp
		state = None
print energy / 1000
cur.execute("select battery_level from chargestates;")
energy = 0
print "----------------"
data = list(cur.fetchall())
last_percentage = int(data[0][0])
for percentage in data[1:]:
	percentage = int(percentage[0])
	if percentage < last_percentage:
		last_percentage = percentage
	elif percentage > last_percentage:
		energy += 0.85 * (percentage - last_percentage)
		last_percentage = percentage
print energy
conn.close()
