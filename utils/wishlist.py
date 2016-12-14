import sqlite3
import os
import steam_api

def is_on_sale(x):
    gd = steam_api.get_gamedata(x)
    print gd
    return gd[2]

def getWishlist(username):
    games = []
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    data = c.execute("SELECT game FROM wishlist WHERE username=?",(username,))
    for x in data:
        games.append(x[0])
    db.close()

    print "Games:", games
    on_sale = filter(is_on_sale, games)
    non_sale = filter(lambda x: not is_on_sale(x), games)
    return on_sale, non_sale


def addWishlist(username,game):
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    data = c.execute("INSERT INTO wishlist VALUES(?,?)",(username,game))
    db.commit()
    db.close()

def removeWishlist(username,game):
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    data = c.execute("DELETE FROM wishlist WHERE username=? AND game=?",(username,game))
    db.commit()
    db.close()

def clearWishlist(username):
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    data = c.execute("DELETE FROM wishlist WHERE username=?", (username,))
    db.commit()
    db.close()

#debug
if __name__ == '__main__':
    os.chdir("..")
    clearWishlist("jones")
    addWishlist("jones",730)
    addWishlist("jones", 225540)
    x = getWishlist("jones")
    print x
    removeWishlist("jones", 730)
    removeWishlist("jones", 225540)
