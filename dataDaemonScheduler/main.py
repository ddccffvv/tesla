'''

	Main starting point for the dataDaemon

'''

from util import log, debug
import databasehandler
import logger
import time
import schedulemanager
from config import DEBUG

class dataDaemon():

	def __init__(self):
		if DEBUG:
			debug.debug("Loading databasehandler & logger")
		self.databasehandler = databasehandler.DatabaseHandler(self)
		self.logger = logger.Logger(self)

		if DEBUG:
			debug.debug("Loading complete")
			debug.debug("Starting the schedule manager")
		self.schedulemanager = schedulemanager.ScheduleManager(self)
		
		if DEBUG:
			debug.debug("Schedule managr is loading, resorting to loop to keep the process alive")

	def getDatabaseHandler(self):
		return self.databasehandler		

	def log(self, msg):
		self.logger.log(msg)


if __name__ == "__main__":
	if DEBUG:
		debug.debug("Starting the dataDaemon")
	dd = dataDaemon()
	while True:
		time.sleep(2)
		# We need this
		if DEBUG:
			debug.debug( "Still running")
