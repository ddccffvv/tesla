'''

Configuration

'''

ENVIRON = "dev" # Change to prod for production
ENVIRON = "prod" # Change to prod for production
#DEBUG = False
DEBUG = True 
if ENVIRON == "dev":
	db_location="localhost"
	db_username="root"
	db_password="toor"
	db_database="smartcharger"

elif ENVIRON == "prod":
	db_location ="localhost"
	db_username = "tesla"
	db_password = "tesla"
	db_database = "tesla"
