def get_timestamp():
        import time, datetime
        return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

def debug(msg):
	f = open("../logs/datadaemonscheduler", "a")
        f.write("[" + get_timestamp() + "] -- DEBUG -- " + str(msg) + "\n")
	f.close()

