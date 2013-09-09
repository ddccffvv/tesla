
from apscheduler.scheduler import Scheduler

from account import Account

import logging
logging.basicConfig()

class ScheduleManager():


	def __init__(self, parent):
		self.parent = parent
		self.accounts = []
		self.jobs = []
		self.metajobs = []
		#self.createCarObjects()

		self.sched = Scheduler()

		self.createCarObjects()

		self.sched.add_interval_job(self.createCarObjects, minutes=5)

		self.sched.start()


	def createCarObjects(self):
		dataaccounts = self.parent.getDatabaseHandler().executeQuery("SELECT accountid, username, updateinterval FROM TeslaCredentials",())

		for dataaccount in dataaccounts:
			accountid = dataaccount[0]
			username = dataaccount[1]
			updateinterval = dataaccount[2]
			
			hit = False
			for account in self.accounts:
				if account.accountid == accountid and account.username == username and updateinterval == account.updateinterval:
					hit = False

			if not hit:
				self.accounts.append(Account(self, accountid, username, updateinterval))


		self.startAllAccounts()

	
	def startAllAccounts(self):
		
		for account in self.accounts:
			if not account.running:
				# We schedule the task
				account.prepareJob()
				account.runMetaJob()
				self.jobs.append (self.sched.add_interval_job( self.runjob, args=[account], seconds= int(account.updateinterval)) )
				self.metajobs.append( self.sched.add_interval_job (self.runMetajob, args=[account], minutes= 30) )
				account.running = True

	def runjob(self, account):
		# Running the job at hand :)
		account.runJob()

	def runMetajob(self, account):
		# Running a different job, the meta one
		account.rubMetaJob()

	def log(self, msg):
		self.parent.log(msg)	
