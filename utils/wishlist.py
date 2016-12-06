import sqlite3
import os

def getWishlist(username):
    ans = []
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    data = c.execute("SELECT username,games FROM wishlist WHERE username=?",(username,))
    for x in data:
        ans.append(x)
    db.close()
    return ans

    
def addWishlist(username,game):
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    data = c.execute("INSERT INTO wishlist VALUES(?,?)",(username,game,))
    db.commit()
    db.close()
    
def removeWishlist(username,game):
    

    

'''
os.chdir("..")
addWishlist("hello","a")
addWishlist("hello","ab")
addWishlist("hello","abc")
addWishlist("jones","abc")
x = getWishlist("hello")
print(x)
x = getWishlist("jones")
print(x)
'''