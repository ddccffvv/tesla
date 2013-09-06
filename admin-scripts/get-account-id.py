
#script to add a user
import MySQLdb as mysql
from optparse import OptionParser
import sys

usage = "usage: %prog [options]"
parser = OptionParser(usage=usage)
parser.add_option("-u", "--username", dest="username", help="The username")

(options, args) = parser.parse_args()

if not options.username:
	print "Please provide a username"
	sys.exit()

connection = mysql.connect("localhost", "tesla", "tesla", "tesla")
cursor = connection.cursor()

cursor.execute("SELECT accountid from users where username like %s", (options.username,))
print "This is the accountid for " + options.username + ":"
for accountid in cursor.fetchall():
	print accountid[0]
connection.close()

