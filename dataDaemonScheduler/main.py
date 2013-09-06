'''

	Main starting point for the dataDaemon

'''

import databasehandler
import logger

import schedulemanager

class dataDaemon():

	def __init__(self):
		self.databasehandler = databasehandler.DatabaseHandler(self)
		self.logger = logger.Logger(self)

		self.schedulemanager = schedulemanager.ScheduleManager(self)

	def getDatabaseHandler(self):
		return self.databasehandler		

	def log(self, msg):
		self.logger.log(msg)


if __name__ == "__main__":
	dd = dataDaemon()
