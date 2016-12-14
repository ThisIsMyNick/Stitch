import httplib, urllib, base64, json

def key():
	k = open("keys.csv", "r").readline();
	k = k.split(",")[2]
	return k

    
 