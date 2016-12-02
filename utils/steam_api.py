import requests
import json

def parse_featured(s):
    d = json.loads(s)
    return d

def get_featured():
    r = requests.get("http://store.steampowered.com/api/featured")
    featured = parse_featured(r.text)
    return featured
