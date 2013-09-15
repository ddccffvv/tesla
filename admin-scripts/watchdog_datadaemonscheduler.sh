#!/bin/bash

pid=`ps aux | grep datadaemonscheduler.py | grep -v grep | perl -ne 'chomp and print'`;

filename="/home/alice/tesla/dataDaemonScheduler/datadaemonscheduler.py";

if [ -z "$pid" ]; then
	nohup /usr/bin/python $filename 
fi
