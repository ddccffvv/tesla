import sqlite3
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
conn.close()
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

