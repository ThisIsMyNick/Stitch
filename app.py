from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3
import os
import utils.steam_api as steam_api
from utils.search import get_id
from pprint import pprint

app = Flask(__name__)

@app.route('/')
def homepage():
    #pprint(steam_api.get_featured())
    feat = steam_api.get_featured()
    games = []
    for game in feat['featured_win']:
        name = game['name']
        price = str(game['final_price'])
        price = price[:-2] + "." + price[-2:]
        games.append((name, price))
    return render_template('homepage.html', game_data=games)#, regRet = regRet)

@app.route('/search/', methods=['GET'])
def search():
    query = request.args.get('query')
    query = query.replace('%', ' ') 
    gameList = get_id(query)
    return render_template('homepage.html',game_data=gameList)

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

@app.route('/authenticate', methods=['POST'])
def authenticate():
    pw = request.form["pass"]
    un = request.form["user"]
    tp = request.form["action"]#login vs. register
    
    if tp == "register":
        regRet = auth.register(un,pw)#returns an error/success message
        return redirect('login.html', result = regRet)
        
    if tp == "login":
        text = auth.login(un,pw)#error message
        if text == "":#if no error message, succesful go back home
            session["Username"] = un
            return redirect(url_for('homePage'))
        return render_template('login.html', result = text)
        

@app.route('/profile')
def myProfile():
    username = session["Username"]
    wl = wishlist.getWishlist(username)
    return render_template('profile.html',username=username,wishlist=wl)

@app.route('/profile/<username>')
def profile(username):
    wl = wishlist.getWishlist(username)
    return render_template('profile.html',username=username,wishlist=wl)

@app.route('/<gamepage>')
def gamepage(gamepage):
    pass
