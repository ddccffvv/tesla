from flask.ext.sqlalchemy import SQLAlchemy
from app import db
from sqlalchemy.dialects.mysql import BIGINT, TEXT, DATE

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

	def __repr__(self):
		return '<User %r, %r, %r, %r>' % (self.username, str(self.accountid), str(self.lastlogin), str(self.lastpasswordchange))

class Account(db.Model):
	__tablename__ = "accounts"
	id = db.Column(BIGINT, primary_key=True)
	subscriptionplan = db.Column(TEXT)
	registrationdate = db.Column(DATE)
	subscriptiondate = db.Column(DATE)
	resellerid = db.Column(BIGINT)

	def __repr__(self):
		return '<Account %r %r %r>' % (str(self.id), self.subscriptionplan, str(self.resellerid))
