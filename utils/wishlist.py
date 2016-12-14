import sqlite3
import os

#add to profile (as wishlist table)
def getWishlist(username):
    ans = []
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    data = c.execute("SELECT username,games FROM wishlist WHERE username=?",(username,))
    for x in data:
        ans.append(x)
    db.close()
    return ans

#add to gamepage(+ button)
def addWishlist(username,game):
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    data = c.execute("INSERT INTO wishlist VALUES(?,?)",(username,game,))
    db.commit()
    db.close()

#add to profile (- button)    
def removeWishlist(username,game):
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    data = c.execute("DELETE FROM wishlist WHERE username=? AND games=?",(username,game,))
    db.commit()
    db.close()

#add to gamepage (as table of users w/ that game on wishlist)
def getUsersFor(game):
    ans = []
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    data = c.execute("SELECT username FROM wishlist WHERE games=?",(game,))  
    for x in data:
        ans.append(x)
    db.close()
    return ans
    


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