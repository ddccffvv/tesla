from flask import Flask
from flask import render_template, flash, request, session, redirect, url_for
from flask.ext.bcrypt import Bcrypt
import sqlite3, sys, os
import MySQLdb
import pytesla
import rpyc
import time

#ENVIRON = "prod" # Change to PROD for other stuff
ENVIRON = "dev"
app = Flask(__name__)
bcrypt = Bcrypt(app)

@app.route("/login", methods=["GET", "POST"])
def login():
	error = None
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]

		cursor = dbconnection.cursor()
		cursor.execute("SELECT id, accountid, password from users WHERE username=%s", (username, ))
		content = cursor.fetchone()
		print content
		if content == None:
			error = "Invalid username or password."
		elif not bcrypt.check_password_hash(content[2], password):
			error = "Invalid username or password."
		else:
			# Fetch the car info
			cursor.execute("SELECT id from vehicles WHERE accountid=%s ORDER BY id DESC",(content[1])) # TODO currently only working with a single car
			carid = cursor.fetchone()
			if carid:
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
	session.pop('carid', None)
	session.pop('userid', None)
	session.pop('accountid', None)
	flash('You were successfully logged out')
	return render_template('index.html')

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
	return redirect(url_for("index"))

@app.route("/car_profile", methods=["GET","POST"])
def car_profile():
	success = ""
	if not 'logged_in' in session:
		return redirect(url_for("logout"))
	if not 'userid' in session:
		return redirect(url_for("logout"))
	
	cursor = dbconnection.cursor()
	
	if request.method == "POST":
		# Adding the content
		tesla_username = request.form["tesla_email"]
		tesla_password = request.form["tesla_password"]

		# We will fetch the pytesla stuff ourselves to check
		try:
			pyobj = pytesla.Connection(tesla_username, tesla_password)
			cars = 0
			print "--DEBUG -- Connected to tesla"
			for vehicle in pyobj.vehicles():
				carid = vehicle.id
				vinnumber = vehicle.vin
				try:
					carmobile = vehicle.mobile_enabled
				except:
					# Car could be asleep waiting
					# Sleep?
					carmobile = False
				print "-- DEBUG -- All information required found adding it!"
				cursor.execute("INSERT INTO vehicles (accountid, brandid, typeid, vinnumber, countryid, mobile_enabled, carid, updated) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (session["accountid"], 1, 1, vinnumber, 1, carmobile, carid, int(time.time())))
				dbconnection.commit()
				# Insert into credential manager
				con = rpyc.connect("localhost",65123)
				con.root.insertCredentials("Tesla",session["accountid"], [tesla_username, tesla_password])
				con.close()
				cars = cars + 1
			if cars == 1:
				success = "The car has been added successfully"
			elif cars > 1:
				success = str(cars) + " have been added successfully"
			else:
				success = "No car was found!"
		except:
			success = "Failed to connect, please retry or verify the credentials"



	
	
	return render_template('car_profile.html',success = success)
		
@app.route("/change-password", methods=["GET", "POST"])
def change_password():
	#first check if we are logged in...
	if not 'logged_in' in session:
		return redirect(url_for("logout"))
	if not 'userid' in session:
		return redirect(url_for("logout"))
	if request.method == "POST":
		oldpassword = request.form["oldpassword"]
		newpassword1 = request.form["newpassword1"]
		newpassword2 = request.form["newpassword2"]


		cursor = dbconnection.cursor()
		cursor.execute("SELECT password from users WHERE id=%s", (session["userid"]))
		content = cursor.fetchone()
		if content == None:
			error = "Invalid password, please try again."
			return render_template("change_password.html", error=error)
		if newpassword1 != newpassword2:
			error = "Passwords do not match, please try again."
			return render_template("change_password.html", error=error)
		if not bcrypt.check_password_hash(content[0], oldpassword):
			error = "Invalid password, please try again."
			return render_template("change_password.html", error=error)
		# Update the password...
		cursor.execute("update users set password=%s WHERE id=%s",(bcrypt.generate_password_hash(newpassword1)))
		cursor.submit()
		success = "Password succesfully changed"
		return render_template("change_password.html", success=success)
	return render_template("change_password.html")



@app.route("/")
def index():
	if session.get("logged_in"):
		return redirect(url_for("dashboard"))
	elif session.get("signup"):
		flash("Thank you for signing up to our beta program. We'll contact you as soon as a new spot opens up!")
		session["signup"] = False
	return render_template("index.html", title="Welcome to EVCloud", page="index")

@app.route("/about")
def about():
	return render_template("about.html", title="About EVCloud", page="about")

@app.route("/contact", methods=["GET","POST"])
def contact():
	if request.method == "POST":
		# Save the information
		name = request.form["name"]
		email = request.form["email"]
		message = request.form["message"]

		# pending sqlalchemy inclusion
	
		return render_template("contact.html", title="Contact EVCloud", page="contact", success = "Thank you! We will contact you as soon as possible.")
	return render_template("contact.html", title="Contact EVCloud", page="contact", success="")

@app.route("/dashboard")
def dashboard():
	car = False
	if not "logged_in" in session:
		return redirect(url_for("index"))
	if "carid" in session:
		car = True # To handle the alert & link
		cur = dbconnection.cursor()
		cur.execute("select battery_level from ChargeStates WHERE carid=%s;",(session.get("carid")))
		data = list(cur.fetchall())
		cur.execute("select updated FROM ChargeStates WHERE carid=%s;", (session.get("carid")))
		starttime = cur.fetchone()
		starttime = datetime.datetime.fromtimestamp(int(starttime[0]))
		timestamp = {"year":0, "month":0, "day":0, "hour":0, "minute":0}
		timestamp["year"] = starttime.year
		timestamp["month"] = starttime.month
		timestamp["day"] = starttime.day
		timestamp["hour"] = starttime.hour
		timestamp["minute"] = starttime.minute

		cur.execute("select latitude,longitude,updated from DriveStates WHERE carid=%s;",(session.get("carid")))
		lat_long = list(cur.fetchall())
		data = "[ " + ",".join(map(lambda x: str(x[0]), data)) + " ]"
		d = defaultdict(list)
		for (latitude, longitude, updated) in lat_long:
			time = datetime.datetime.fromtimestamp(int(updated))
			d[str(time.year) + "/" + str(time.month) + "/"+ str(time.day)].append((latitude, longitude))

		lat_long = []
		for k, v in d.iteritems():
			print k
			dist = 0
			for i,j in zip(v[0::2],v[1::2]):
				dist +=  float(distance(i,j))
			print "total: " + str(dist)
			lat_long.append((k, str(dist)))
		return render_template("test.html", data = data, timestamp= timestamp, entries=lat_long, page="dashboard", title="Dashboard",car=car)
	else:
		return render_template("test.html", data = "[]", timestamp= None, entries=[], page="dashboard", title="Dashboard", car=car)

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
    	app.run(host='0.0.0.0',debug=True,port=4343)
