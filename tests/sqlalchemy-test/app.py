from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import BIGINT, TEXT, DATE, INTEGER, TINYINT
from config import db_location, db_username, db_password, db_database

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' + db_username + ":" + db_password + "@" + db_location + "/" + db_database
db = SQLAlchemy(app)


class User(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(TEXT)
	password = db.Column(TEXT)
	accountid = db.Column(BIGINT) #, db.ForeignKey('account.id'))
	#account = db.relationship('Account', backref=db.backref('users', lazy="dynamic"))
	#foreign keys do not work because not defined in the database
	lastlogin = db.Column(DATE)
	lastpasswordchange = db.Column(DATE)

	def __init__(self, username, password, accountid, lastlogin, lastpasswordchange):
		self.username = username
		self.accountid = accountid
		self.password = password
		self.lastlogin = lastlogin
		self.lastpasswordchange = lastpasswordchange

	def get_account(self):
		return Account.query.filter_by(id=self.accountid).first()

	def __repr__(self):
		return '<User %r, %r, %r, %r>' % (self.username, str(self.accountid), str(self.lastlogin), str(self.lastpasswordchange))

class Account(db.Model):
	__tablename__ = "accounts"
	id = db.Column(BIGINT, primary_key=True)
	subscriptionplan = db.Column(TEXT)
	registrationdate = db.Column(DATE)
	subscriptiondate = db.Column(DATE)
	resellerid = db.Column(BIGINT)

	def get_users(self):
		return User.query.filter_by(accountid = self.id).all()

	def __repr__(self):
		return '<Account %r %r %r>' % (str(self.id), self.subscriptionplan, str(self.resellerid))

class Vehicle(db.Model):
	__tablename__ = "vehicles"
	id = db.Column(BIGINT, primary_key=True)
	accountid = db.Column(BIGINT)
	brandid = db.Column(BIGINT)
	typeid  = db.Column(BIGINT)
	licenseplate = db.Column(TEXT)
	vinnumber = db.Column(TEXT)
	carid = db.Column(TEXT)
	updated = db.Column(TEXT)
	constructionyear = db.Column(DATE)
	countryid = db.Column(INTEGER)
	mobile_enabled = db.Column(TINYINT)

	def __repr__(self):
		return '<Vehicle %r %r %r %r %r>' % (str(self.id), str(self.accountid), str(self.licenseplate), self.carid, self.updated)

class ChargeState(db.Model):
	__tablename__ = "chargestates"
	id = db.Column(BIGINT, primary_key=True)

class DriveState(db.Model):
	__tablename__ = "drivestates"
	id = db.Column(BIGINT, primary_key=True)


@app.route("/")
def index():
	users = User.query.all()	
	print Account.query.all()
	print Vehicle.query.all()
	print users[0].get_account()
	print Account.query.all()[0].get_users()
	return "test"

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True, port=4343)
