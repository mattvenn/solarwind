import requests
from CosmFeedUpdate import *

url = 'http://www.swpc.noaa.gov/ftpdir/lists/ace/ace_swepam_1m.txt'
feed_id = "1466087133"
def fetch_speed():
    r = requests.get(url)
    if r.status_code == 200:
        text = r.text.splitlines()
        latest = text[-1]
        fields = latest.split()
        if int(fields[6]) == 0:
            return(fields[0:4],fields[8])
        else:
            print "bad data:", latest
            exit(1)
    else:
        print "couldn't fetch page:", r.status_code
        exit(1)

(date,speed) = fetch_speed()
print "current solar wind speed: ", speed

#private key stored in a file
keyfile="api.key"
key=open(keyfile).readlines()[0].strip()

pfu = CosmFeedUpdate(feed_id,key)
pfu.addDatapoint('speed', speed)

# finish up and submit the data
pfu.buildUpdate()
pfu.sendUpdate()

