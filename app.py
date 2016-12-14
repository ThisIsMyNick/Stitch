from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3
import os
import utils.steam_api as steam_api
from utils.search import get_id
from pprint import pprint
from utils import login, wishlist   

app = Flask(__name__)

"""
game_data:
[name, price, discounted (bool), discount %, image]
"""
@app.route('/')
def homepage():
    feat = steam_api.get_featured()
    error = request.args.get('error')
    print error
    success = request.args.get('success')
    return render_template('homepage.html', game_data=feat, session=session, success=success,error=error)

@app.route('/search/', methods=['GET'])
def search():
    query = request.args.get('query')

    if not query:
        return render_template("homepage.html")
    ids = get_id(query)
    results = []
    for id_ in ids:
        d = steam_api.get_gamedata(id_[1])
        if d:
            results.append(d)
    pprint(results)
    return render_template('homepage.html',game_data=results)


@app.route('/authenticate/', methods=['POST'])
def authenticate():
    pw = request.form["pass"]
    un = request.form["user"]
    tp = request.form["action"]#login vs. register
    
    if tp == "register":
        regRet = login.register(un,pw)#returns an error/success message
        if regRet == 1:
            return redirect(url_for('homepage',success="You have registered"))
        else:
            return redirect(url_for('homepage',error=regRet))
        
    if tp == "login":
        text = login.login(un,pw)#error message
        if text == "":#if no error message, succesful go back home
            session["Username"] = un
            print('Username' not in session)    
            return redirect(url_for('homepage',success="You have logged in"))
        return redirect(url_for('homepage',error=text))
    

@app.route('/profile/')
def myProfile():
    if 'Username' in session:
        username = session["Username"]
        wl = wishlist.getWishlist(username)
        return render_template('profile.html',username=username,wishlist=wl)
    else:
        return redirect(url_for('homepage',error="You must log in first"))
        
        
@app.route('/profile/<username>')
def profile(username):
    wl = wishlist.getWishlist(username)
    return render_template('profile.html',username=username,wishlist=wl)

@app.route('/<gamepage>')
def gamepage(gamepage):
    return '123'
    
@app.route("/logout/")
def logout():
    if "Username" in session:# can only log out if you are already logged in
        session.pop("Username")
    return redirect (url_for('homepage',success="Logged out"))

if __name__ == '__main__':
    if os.path.getsize("data/database.db") == 0:
        f = "data/database.db"
        db = sqlite3.connect(f, check_same_thread=False)
        c = db.cursor()
        print "Initializing database"
        c.execute("CREATE TABLE users (username TEXT, password TEXT)")
        c.execute("CREATE TABLE wishlist (username TEXT, games TEXT)")
        db.commit()
        db.close()
    app.debug=True
    app.secret_key = '  \x43\xd2\x34\x92\x5b\x4a\x80\xfc\xc6\xb0\x0e\x45\xdd\x51\x36\xc0\xd2\x3a\x85\x42\x57\xbb\x61\xf2\x7b\xb6\xfc\x17\x3b\x1a\xda\x5b\x6d\x7d\x0a\xff\xd3\x6f\xfa\x7c\x1b\xa8\x0f\x7f\x53\x18\x8d\x91\x16\x81'
    app.run()
