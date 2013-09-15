#!/bin/bash

pid=`ps aux | grep credentialmanager.py | grep -v grep | perl -ne 'chomp and print'`;

filename="/home/alice/tesla/CredentialMgr/credentialmanager.py";

if [ -z "$pid" ]; then
	#nohup /usr/bin/python $filename 
fi
