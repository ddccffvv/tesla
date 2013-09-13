#!/usr/bin/python

import subprocess
import re

p = subprocess.Popen(["ps", "aux"], stdout=subprocess.PIPE)
output, err = p.communicate()
for x in output.split("\n"):
	regex = re.compile(r".* datadaemonscheduler.py.*")
	if regex.match(x):
		p 
#filename="/home/alice/tesla/dataDaemonScheduler/datadaemonscheduler.py";
#
#if $pid ;
#then
#	python $filename &
#fi
