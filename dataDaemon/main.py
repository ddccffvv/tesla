

'''

	The main loader of the daemon
	This should become the default daemon process

'''


# Steps required
# 	1. Setup the database connection class
#	2. Create the default objects (the user that exist on the system)
#	3. Create the structure of the threads + the connection handling and more
#	4. Correct and rotate
#	5. Enjoy a beer


from databasehandler import DatabaseHandler
from logger import Logger
from threadmanager import ThreadManager

class dataDaemon():

	def __init__(self):
		self.databaseh = DatabaseHandler(self)
		self.logger = Logger(self)

		# All relevant objects have been created, except the general thread generator
		self.threadmanager = ThreadManager(self)		
		


	def getDatabaseHandler(self):
		return self.databaseh
	
	def log(self, msg):
		# Create a log output
		self.logger.log(msg)

	def KeepRunning(self):
		fileh = open("commands.txt","r")
		content = "".join(fileh.readlines())
		fileh.close()
		print content
		if content.find("quit") > -1:
			return False
		else:

			return True	

if __name__ == "__main__":
	dD = dataDaemon()
