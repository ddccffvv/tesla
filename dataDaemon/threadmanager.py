
from account import Account

from teslathread import TeslaThread

from credentialforcer import CredentialForcer

class ThreadManager():


	def __init__(self, parent):
		self.parent = parent
		self.accounts = []
		self.threads = []
		self.__createCredentialObjects()
		
		self.credentialforcer = CredentialForcer(self.parent, self)
		self.credentialforcer.start()


	

	def log(self, msg):
		self.parent.log(msg)

	def __createCredentialObjects(self):
		# Get all the account object at startup
		# atm only tesla objects
		dbh = self.parent.getDatabaseHandler()
		results = dbh.executeQuery("SELECT accountid, username, password, updateinterval FROM TeslaCredentials")
		for res in results:
			accountid = res[0]
			username = res[1]
			password = res[2]
			updateinterval = res[3]
			self.accounts.append(Account(accountid, username, password, updateinterval))		


		self.__startThreads()

	def verifyCredentials(self):
		dbh = self.parent.getDatabaseHandler()
		results = dbh.executeQuery("SELECT accountid, username, password, updateinterval from TeslaCredentials")
		for res in results:
			accountid = res[0]
			username = res[1]
			password = res[2]
			updateinterval = res[3]
			for account in self.accounts:
				if account.Accountid != accountid and account.TeslaCredentials != [username, password]:
					# New credentials found!
					self.log("New ste of credentials found")
					self.accounts.append(Account(accountid, username, password, updateinterval))

		self.__startThreads()

	def __startThreads(self):
		for account in self.accounts:
			if not account.isRunning():
				print "Launching thread"
				temp = TeslaThread(account, self.parent)
				self.threads.append(temp)
				temp.start()
			
