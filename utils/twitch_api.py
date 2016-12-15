import httplib, urllib2, base64, json, urllib
from utils.steam_api import get_gamedata
def keys():
	k = open("keys.csv", "r").readline();
	k = k.split(",")
	return k

def retrieveStream(gameID):
    name = steam_api.get_gamedata(gameID)[0]
    key = keys()
    req = {
            'query':name,
            'client_id':key[0],
            'limit':1
          }
          
    querystring = urllib.urlencode(req)
    url = 'https://api.twitch.tv/kraken/search/channels?' + querystring
    x = urllib2.urlopen(url)
    data = json.loads(x.read())
    print name
    return data['channels'][0]['name'] 


if __name__ == '__main__':
    import os, steam_api
    os.chdir('..')
    print(retrieveStream(730))
    