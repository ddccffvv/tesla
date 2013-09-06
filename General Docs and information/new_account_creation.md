Create a new set of credentials in the database
==============

1. Insert Reseller
Before entering a new account, we need to make sure the reseller is in place. Currently 1 is us


SELECT id from resellers WHERE name="EVCloud"


2. Insert Accounts
Accounts are just a master entry for all users (bit like 1 account multiple users)


INSERT INTO accounts (subscriptionplan, registrationdata, subscriptiondata, resellerid) VALUES (1, NOW(), NOW(), <result step 1>)
SELECT id from accounts ORDER BY id DESC LIMIT 0, 1	# Select the last id, maybe this requires a bit more work

3. Insert User Account
Now you can insert the user account


INSERT INTO users (accountid, username, password, lastlogin, lastpasswordchange) VALUES (<result step 2>, <username>, <password>, "","")


3b optional: Insert user information


Fields: 
* userid
* firstname
* middlename
* lastname
* addresso
* addresst
* zipcode
* city
* countryid --> linked to table: countries
* stateid --> linked to table: states
* phone
* mobile
* fax
* email

4. Insert car & credentials
This takes a bit more work :)
First you need to add the new car in the table vehicles

Fields:
* accountid --> you know this
* brandid --> linked to table : vehiclebrands (e.g. Tesla)
* typeid --> linked to table: vehicletypes (e.g. Model S)
* licenseplate (Filled in by the dataDaemon)
* vinnumber (Filled in by the dataDaemon)
* constructionyear
* countryid --> linked to table: countries
* mobile_enabled (Filled in by the dataDaemon)
* carid (Filled in by the dataDaemon) (You will see this field more in other tables, however in other table the reference carid is linked to the id from this table, not this field!!)
* updated (Filled in by the dataDaemon)

After the car has been added, we need to add the credentials in the table TeslaCredentials

Fields:
* accountid  --> you know this
* username
* password (this should be a dummy)
* updated (now())
* updateinterval (the interval for the refresh/adding of the data in the backend)

Now the new bit, you need to tell the credentialmanager to add the credentials since he will be doing to actual login
The code below is how to do it in python

	import rpyc
	c = rpyc.connect("localhost",65123)
	accountid = <you know by now>
	cartype = "Tesla" # This is just to make it a bit more future proof
	credentials = [username, password]
	c.root.insertCredentials( cartype, accountid, credentials)
	c.close()

This is it! From now on the data will be fetche dand users are able to login


