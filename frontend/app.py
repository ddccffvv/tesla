from flask import Flask
from flask import render_template, flash, request, session, redirect, url_for
import sqlite3, sys, os
import MySQLdb

ENVIRON = "dev" # Change to PROD for other stuff
app = Flask(__name__)

@app.route("/login", methods=["GET", "POST"])
def login():
	error = None
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]

		cursor = dbconnection.cursor()
		cursor.execute("SELECT id, accountid from users WHERE username=%s and password=%s", (username, password))
		content = cursor.fetchone()
		if content == None:
			error = "Invalid username or password."
		else:
			# Fetch the car info
			cursor.execute("SELECT id from vehicles WHERE accountid=%s ORDER BY id DESC",(content[1])) # TODO currently only working with a single car
			carid = cursor.fetchone()
			session['carid'] = carid[0]
			session['logged_in'] = True
			session['username'] = username
			session["userid"] = content[0]
			session["accountid"] = content[1]
			flash("You were logged in")
			return redirect(url_for("index"))
	return render_template("login.html", error=error)

@app.route("/logout")
def logout():
	session.pop('logged_in', None)
	session.pop('username', None)
	flash('You were successfully logged out')
	return redirect(url_for('index'))

@app.route("/details")
def details():
	return render_template("details.html")

@app.route("/signup", methods=["POST"]) # Get is simply blocked as 404
def signup():
	email = request.form["email"]
	fileh = open("signups.txt","a")
	fileh.write(email + "\n")
	fileh.close()
	session["signup"] = True
	# TODO fix this into a proper message
	flash("Thank you for signing up to our beta program. When new spots are available you might be contacted.")
	return redirect(url_for("index"))

@app.route("/")
def index():
	if session.get("logged_in"):
		return bla(session.get("accountid"))
	elif session.get("signup"):
		flash("Thank you for signing up to our beta program. When new spots are available you might be contacted.")
		session["signup"] = False
	return render_template("index.html", title="Welcome to EVCloud")

@app.route("/about")
def about():
	return render_template("about.html", title="About EVCloud", page="about")

@app.route("/contact")
def contact():
	return render_template("contact.html", title="Contact EVCloud", page="contact")

def bla(accountid):
	#conn = sqlite3.connect('/home/alice/tesla_aggregator_bart/tesla_data.db')
	cur = dbconnection.cursor()
	cur.execute("select battery_level from ChargeStates WHERE carid=%s;",(session.get("carid")))
	data = list(cur.fetchall())
	cur.execute("select latitude,longitude,updated from DriveStates WHERE carid=%s;",(session.get("carid")))
	lat_long = list(cur.fetchall())
	data = "[ " + ",".join(map(lambda x: str(x[0]), data)) + " ]"
	d = defaultdict(list)
	for (latitude, longitude, updated) in lat_long:
		time = datetime.datetime.fromtimestamp(int(updated))
		d[str(time.year) + str(time.month) + str(time.day)].append((latitude, longitude))

	lat_long = []
	for k, v in d.iteritems():
		print k
		dist = 0
		for i,j in zip(v[0::2],v[1::2]):
			dist +=  float(distance(i,j))
		print "total: " + str(dist)
		lat_long.append((k, str(dist)))
	return render_template("test.html", data = data, entries=lat_long, page="dashboard", title="Dashboard")
    #except:
	#print "Unexpected error:", str(sys.exc_info()[0].message)
        #return "error..."

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

if __name__ == "__main__":

	# Setup sql connection
	if ENVIRON == "dev":
		db_location = "localhost"
		db_username = "root"
		db_password = "toor"
		db_database = "smartcharger"
	elif ENVIRON == "prod":
		db_location = "localhost"
		db_username = "tesla"
		db_password = "tesla"
		db_database = "tesla"	
	else:
		sys.exit(1)
	dbconnection = MySQLdb.connect(db_location, db_username, db_password, db_database)
	
	app.secret_key = os.urandom(30)
    	app.run(host='0.0.0.0',debug=True,port=8080)
