import sqlite3


def getWishlist(username):
    ans = []
    db = sqlite3.connect("data/database.db")
    c = db.cursor()
    data = c.execute("SELECT username,games FROM wishlist WHERE username=?",(username,))
    for x in data:
        ans.append(x)
    return ans

    