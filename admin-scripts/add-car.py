
#script to add a user
import MySQLdb as mysql
from optparse import OptionParser

usage = "usage: %prog [options]"
parser = OptionParser(usage=usage)
parser.add_option("-u", "--username", dest="username", help="The username")
parser.add_option("-p", "--password", dest="password", help="The password")

(options, args) = parser.parse_args()

connection = mysql.connect("localhost", "tesla", "tesla", "tesla")
cursor = connection.cursor()

print "under construction"
connection.commit()
connection.close()

