#!/bin/bash

data=`ps aux | grep -e "python.*datadaemonscheduler.py" | grep -v grep | tr -s ' ' | cut -d" " -f 2`
cred=`ps aux | grep -e "python.*credentialmanager.py" | grep -v grep | tr -s ' ' | cut -d" " -f 2`

if [ -z "$data" ]; then
	echo -e "\e[1;31m[ERROR] Datadaemonscheduler not running.\e[0m"
else
	echo -e "\e[1;32m[OK] Datadaemonscheduler running. ($data)\e[0m"
fi
if [ -z "$cred" ]; then
	echo -e "\e[1;31m[ERROR] Credentialmanager not running.\e[0m"
else
	echo -e "\e[1;32m[OK] Credentialmanager running. ($cred)\e[0m"
fi
