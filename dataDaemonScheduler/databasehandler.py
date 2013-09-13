

from config import db_location, db_username, db_password, db_database
import MySQLdb as mysql

class DatabaseHandler():

	def __init__(self, parent):
		self.parent = parent

	def executeQueryNoResult(self, query, parameters=None, commit=False):
		self.connection = mysql.connect(db_location, db_username, db_password, db_database)
		cursor = self.connection.cursor()
		if parameters == None:
			cursor.execute(query)
		else:
			cursor.execute(query, parameters)
		if commit:
			self.connection.commit()
		self.connection.close()

	def executeQuery(self, query, parameters=None, commit=False):
		self.connection = mysql.connect(db_location, db_username, db_password, db_database)
		cursor = self.connection.cursor()
		if parameters == None:
			cursor.execute(query)
		else:
			cursor.execute(query, parameters)

		if commit:
			self.connection.commit()

		bla = cursor.fetchall()
		self.connection.close()
		return bla
