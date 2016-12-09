from pprint import pprint
import sys
sys.path.append('../utils/')
import steam_api
import json

feat = steam_api.get_featured()
pprint(feat)
