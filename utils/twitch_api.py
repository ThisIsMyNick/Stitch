import httplib, urllib2, base64, json, urllib
from utils.steam_api import get_gamedata
def keys():
	k = open("keys.csv", "r").readline();
	k = k.split(",")
	return k

def getStreamName(gameID):
    x = get_gamedata(gameID)
    if not x:
        return -1
    name = x[0]
    key = keys()
    req = {
            'query':name,
            'client_id':key[0],
            'limit':25
          }
          
    querystring = urllib.urlencode(req)
    url = 'https://api.twitch.tv/kraken/streams?' + querystring
    #print url
    x = urllib2.urlopen(url)
    data = json.loads(x.read())
    #print name
    if data["_total"] > 0:
        for x in data['streams']:
            if x['game'] == name:
                print x
                return x['channel']['name']
        return -1
    else:
        return -1


    