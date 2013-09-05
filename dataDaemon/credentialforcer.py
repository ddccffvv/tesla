'''

	This thread is responsible of updating the list of threads. It will force the threadmanager to look in the database and initiate the new notrunning credentials

'''


import threading
import time

class CredentialForcer(threading.Thread):

	def __init__(self, parent, threadmanager):
		threading.Thread.__init__(self)
		self.parent = parent
		self.threadmanager = threadmanager
		self.sleepperiod = 60*2
		

	def run(self):
		# While loop and we just keep looping
		while self.parent.KeepRunning():
			self.threadmanager.verifyCredentials()
			time.sleep(self.sleepperiod)
