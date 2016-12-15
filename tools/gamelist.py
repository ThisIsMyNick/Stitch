import urllib2
import requests
import sqlite3
from lxml import html
import time
import os

games = {}

def getpage(pg):
    if pg == 1:
        page = ""
    else:
        page = "page" + str(pg) + "/"
    #u = urllib2.urlopen("https://steamdb.info/apps/" + page)
    r = requests.get('https://steamdb.info/apps/' + page)
    tree = html.fromstring(r.content)

    # app_ids = tree.xpath('//*[@id="table-apps"]/tbody/tr/td/a/text()')
    # app_types = tree.xpath('//*[@id="table-apps"]/tbody/tr/td[2]/text()')
    # app_names = tree.xpath('//*[@id="table-apps"]/tbody/tr/td[3]/text()')
    #only get items that are in steam store
    app_ids = tree.xpath(
        '//*[@id="table-apps"]/tbody/tr/td[3]/a/span/../../../td/a/text()')
    app_types = tree.xpath(
        '//*[@id="table-apps"]/tbody/tr/td[3]/a/span/../../../td[2]/text()')
    app_names = tree.xpath(
        '//*[@id="table-apps"]/tbody/tr/td[3]/a/span/../../../td[3]/text()')

    app_ids = [x.strip() for x in app_ids]
    app_types = [x.strip() for x in app_types]
    app_names = [x.strip() for x in app_names]

    app_ids = filter(lambda x: x != '', app_ids)
    app_types = filter(lambda x: x != '', app_types)
    app_names = filter(lambda x: x != '', app_names)

    apps = zip(app_ids, app_types, app_names)
    apps = filter(lambda x: x[1] == 'Game', apps)
    global games
    for app in apps:
        games[app[0]] = app[2]
    print pg
    # print apps

def gamelist():
    for i in range(1,662):
        getpage(i)
        time.sleep(1)
    gamelist = zip(games.keys(), games.values())
    gamelist = [(x[1], x[0]) for x in gamelist]
    sorted_gl = sorted(gamelist, key=lambda x:x[0])
    return sorted_gl

if __name__ == '__main__':
    db = sqlite3.connect("app_ids.db")
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS apps (name TEXT, id INTEGER, UNIQUE(name,id))")
    gl = gamelist()
    for g in gl:
        c.execute("INSERT OR IGNORE INTO apps VALUES(?,?)", (g[0], g[1]))
    db.commit()
    db.close()
    print "Done. Move app_ids.db to data/ to use it."
