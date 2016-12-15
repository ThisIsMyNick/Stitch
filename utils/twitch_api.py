import httplib, urllib2, base64, json
from utils.steam_api import get_gameData
def keys():
	k = open("keys.csv", "r").readline();
	k = k.split(",")
	return k

def retrieveStream(gameID):
    name = get_gameData(gameID)[0]
    keys = keys()
    req = {
            'client_id':keys[0]
          }
    x = urllib2.urlopen()


if __name__ == '__main__':
    import os
    os.chdir('..')
