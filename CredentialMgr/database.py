
import sqlite3
import base64

class Database():

	def __init__(self):
		self.connection = sqlite3.connect("credentialvault")
	
		try:
			cursor = self.connection.cursor()
			cursor.execute("SELECT * FROM keystore")
		except:
			self.__setupDB()


	def __setupDB(self):
		cursor = self.connection.cursor()
		cursor.execute("CREATE TABLE keystore (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, data TEXT, datap TEXT, accountid TEXT, cartype TEXT)")

		self.connection.commit()


	def getCredentials(self, accountid, cartype="Tesla"):
		cursor = self.connection.cursor()
		cursor.execute("SELECT data,datap from keystore WHERE accountid=? and cartype=?", (accountid, cartype))
		data = cursor.fetchone()
		return [base64.b64decode(data[0]), base64.b64decode(data[1])]

	def insertCredentials(self, accountid, credentials, cartype):
		cursor = self.connection.cursor()
		cursor.execute("INSERT INTO keystore (data, datap, accountid, cartype) VALUES (?,?,?,?)", (base64.b64encode(credentials[0]), base64.b64encode(credentials[1]), accountid, cartype))
		self.connection.commit()

