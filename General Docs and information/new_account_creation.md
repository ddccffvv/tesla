Create a new set of credentials in the database
==============

1. Insert Reseller
Before entering a new account, we need to make sure the reseller is in place. Currently 1 is us

SELECT id from resellers WHERE name="EVCloud"


2. Insert Accounts
Accounts are just a master entry for all users (bit like 1 account multiple users)

INSERT INTO accounts (subscriptionplan, registrationdata, subscriptiondata, resellerid) VALUES (1, NOW(), NOW(), <result step 1>)


