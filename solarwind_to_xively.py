#!/usr/bin/python

import requests
from CosmFeedUpdate import *
import fcntl
import logging
from xively import xively
feed_id = "1466087133"
url = 'http://services.swpc.noaa.gov/text/ace-swepam.txt'

def fetch_speed():
    r = requests.get(url,timeout=10)
    if r.status_code == 200:
        text = r.text.splitlines()
        latest = text[-2]
        fields = latest.split()
        if int(fields[6]) == 0 and fields[8] != '-9999.9':
            return(fields[0:4],fields[8])
        else:
            print "bad data:", latest
            exit(1)
    else:
        print "couldn't fetch page:", r.status_code
        exit(1)

#locking
file = "/tmp/solarwind.lock"
fd = open(file,'w')
try:
    print "check lock"
    fcntl.lockf(fd,fcntl.LOCK_EX | fcntl.LOCK_NB)
    print "ok"
except IOError:
    print "another process is running with lock. quitting!", file
    exit(1)

(date,speed) = fetch_speed()
print "current solar wind speed: ", date, speed

#private key stored in a file
#keyfile="api.key"
#key=open(keyfile).readlines()[0].strip()

#pfu = CosmFeedUpdate(feed_id,key)
#pfu.addDatapoint('speed', speed)

logging.basicConfig(level=logging.INFO)
xively_t = xively(feed_id, logging)
xively_t.add_datapoint('speed', speed)
xively_t.start()
# finish up and submit the data
#pfu.buildUpdate()
#pfu.sendUpdate()
print "sent"
