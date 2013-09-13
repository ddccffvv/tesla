def get_timestamp():
        import time, datetime
        return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

def log(msg):
        print "[" + get_timestamp() + "] " + str(msg)

