'''

Setup a rpyc to receive calls
Load the credentials when required

'''

import rpyc
from rpyc.utils.server import ThreadedServer
from rpyc.utils.authenticators import AuthenticationError
from util import debug
import database
import pytesla

class CredentialService(rpyc.Service):
	# Do more stuff
	def on_connect(self):
		debug( "Welkom")

	def on_disconnect(self):
		debug( "Bye!")

	def exposed_getLoginToken(self, accountid, cartype="Tesla"):
		dbobject = database.Database()
		credentials = dbobject.getCredentials(accountid, cartype)
		debug( "Got the credentials, logging in and returning object")
		if cartype == "Tesla":
			debug( "here we go for Tesla")
			return pytesla.Connection(credentials[0], credentials[1])
		else:
			return "Something else"

	def exposed_insertCredentials(self, cartype, accountid, credentials):
		##
		dbobject = database.Database()
		dbobject.insertCredentials(accountid, credentials, cartype)
'''
	TODO: not working atm!
'''
def authenticatorMethod(sock):
	debug( "got something!!")
	debug(sock)
	data = sock.recv(10)
	debug( data)
	if data != "0123456789":
		raise AuthenticationError("wrong secret")
	return sock, None

if __name__ == "__main__":
	server = ThreadedServer(CredentialService, port=65123, protocol_config = {"allow_public_attrs": True}) #, authenticator=authenticatorMethod)
	server.start()
