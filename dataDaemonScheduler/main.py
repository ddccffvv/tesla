'''

	Main starting point for the dataDaemon

'''

from config import db_location, db_username, db_password, db_database
import databasehandler


class dataDaemon():

	def __init__(self):
		self.databasehandler = databasehandler.DatabaseHandler(db_location, db_username, db_password, db_database)

	def getDatabaseHandler(self):
		return eslf.databasehandler		



if __name__ == "__main__":
	dd = dataDaemon()
