
import sqlite3
import time

class Logger():


	def __init__(self, parent):
		self.parent = parent
		self.connection = sqlite3.connect("logdb-" + str(int(time.time())) + ".db")

		try:
			cursor = self.connection.cursor()
			cursor.execute("SELECT * FROM Logs LIMIT 0,1")
		except:
			# Fail, setup the database
			self.__setup()

	def __setup(self):
		cursor = self.connection.cursor()
		cursor.execute("""CREATE TABLE [Logs] (
[id] INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
[msg] TEXT  NULL,
[updated] TEXT  NULL
)""")
		self.connection.commit()



	def log(self, msg):
		cursor = self.connection.cursor()
		cursor.execute("INSERT INTO Logs (msg, updated) VALUES (?,?)", (msg, int(time.time())))
		self.connection.commit()
