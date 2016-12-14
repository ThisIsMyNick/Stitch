import httplib, urllib, base64, json
import os
os.chdir('..')
def keys():
	k = open("keys.csv", "r").readline();
	k = k.split(",")
	return k
keys = keys()

x = urllib.urlopen('https://api.twitch.tv/kraken/oauth2/authorize?response_type=code&client_id=%s&redirect_uri=http://127.0.0.1:5000/&scope=chat_login'%(keys[0]))
html = x.read()
print(html)
