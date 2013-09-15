#!/bin/bash

data=`ps aux | grep -e "datadaemonscheduler.py" | grep -v grep`
cred=`ps aux | grep -e "credentialmanager.py" | grep -v grep`

if [ -z "$data" ]; then
	echo -e "\e[1;31m[ERROR] Datadaemonscheduler not running.\e[0m"
else
	echo -e "\e[1;32m[OK] Datadaemonscheduler running.\e[0m"
fi
if [ -z "$cred" ]; then
	echo -e "\e[1;31m[ERROR] Credentialmanager not running.\e[0m"
else
	echo -e "\e[1;32m[OK] Credentialmanager running.\e[0m"
fi
