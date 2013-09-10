
#script to add a user
import MySQLdb as mysql
from optparse import OptionParser
import bcrypt


usage = "usage: %prog [options]"
parser = OptionParser(usage=usage)
parser.add_option("-u", "--username", dest="username", help="The username")
parser.add_option("-p", "--password", dest="password", help="The password")

(options, args) = parser.parse_args()

connection = mysql.connect("localhost", "tesla", "tesla", "tesla")
cursor = connection.cursor()

cursor.execute("INSERT INTO accounts (subscriptionplan, registrationdate, subscriptiondate, resellerid) VALUES (1, NOW(), NOW(), 1)")
connection.commit()
cursor.execute("SELECT id from accounts ORDER BY id DESC LIMIT 0, 1")
account_id = cursor.fetchone()
account_id = account_id[0]
password = bcrypt.hashpw(options.password, bcrypt.gensalt())
cursor.execute("INSERT INTO users (accountid, username, password, lastlogin, lastpasswordchange) VALUES (%s, %s, %s, %s, %s)", (account_id, options.username, password, "", ""))
connection.commit()
connection.close()

print "user added"
