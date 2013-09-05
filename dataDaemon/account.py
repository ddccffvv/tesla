


class Account():

	def __init__(self, accountid, username, password, updateinterval):
		self._accountid = accountid
		self._teslacredentials = [username, password]
		self.updateinterval = updateinterval
		self.running = False

	def getUpdateInterval(self):
		return self.updateinterval

	def setUpdateInterval(self, updateinterval):
		self.updateinterval = updateinterval

	def startRunning(self):
		self.running = True

	def stopRunning(self):
		self.running = False

	def isRunning(self):
		return self.running

	@property
	def Accountid(self):
		return self._accountid

	@Accountid.setter
	def Accountid(self, value):
		self._accountid = value

	@Accountid.deleter
	def Accountid(self):
		del self._accountid

	@property
	def TeslaCredentials(self):
		return self._teslacredentials

	@TeslaCredentials.setter
	def TeslaCredentials(self, username, password):
		self._teslacredentials= [username, password]


	@TeslaCredentials.deleter
	def TeslaCredentials(self):
		del self._teslacredentials
