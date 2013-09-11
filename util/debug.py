def get_timestamp():
        import time, datetime
        return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

def debug(msg):
        print "[" + get_timestamp() + "] -- DEBUG -- " + str(msg)

