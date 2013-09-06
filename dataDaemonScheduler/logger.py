

import time



class Logger():

	def __init__(self, parent):
		self.parent = parent
		self.dbconnection = self.parent.getDatabaseHandler()


	def log(self, msg):
		self.dbconnection.executeQueryNoResult("INSERT INTO logs (process, msg, updated) VALUES (\"dataDaemon\", %s, %s)", (msg, int(time.time())), commit=True)
