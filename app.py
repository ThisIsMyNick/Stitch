from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3
import os
import json
from utils.search import get_id
from utils import login, wishlist,steam_api,twitch_api
from pprint import pprint
import urllib,urllib2


app = Flask(__name__)

"""
game_data:
[name, price, discounted (bool), discount %, image, app_id, steam url]
"""
@app.route('/')
def homepage():
    feat = steam_api.get_featured()
    error = request.args.get('error') 
    success = request.args.get('success') 
    code = ""
    if (request.args.get('code')):
        code = "Twitch connection established"
        keys = twitch_api.keys()
        req = {
            'client_id':keys[0],
            'client_secret':keys[1],
            'grant_type':'authorization_code',
            'redirect_uri':'http://127.0.0.1:5000/',
            'code':request.args.get('code')
        }
        url = 'https://api.twitch.tv/kraken/oauth2/token'
        x = urllib2.urlopen(url,urllib.urlencode(req))
        data = json.loads(x.read())
        session['token'] = data['access_token']
        
    return render_template('homepage.html', game_data=feat, 
                            session=session, success=success,
                            error=error,code=code)

@app.route('/search/', methods=['GET'])
def search():
    query = request.args.get('search')

    if not query:
        return render_template("homepage.html")
    ids = get_id(query)
    results = []
    for id_ in ids:
        d = steam_api.get_gamedata(id_[1])
        if d:
            results.append(d)
    return render_template('search.html',game_data=results)


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


@app.route('/profile/<username>/')
def profile(username):
    if not login.duplicate(username):
        return redirect(url_for('homepage', error="No such user"))
    wl = wishlist.getWishlist(username)
    return render_template('profile.html',username=username,wishlist=wl)

@app.route('/gamepage/<gameid>')
def gamepage(gameid):
    game = steam_api.get_gamedata(gameid)
    streamName = twitch_api.getStreamName(gameid)
    users = wishlist.getUsersFor(gameid)
    success = request.args.get('success')
    
    username = None
    if 'Username' in session:
        username = session["Username"]
    return render_template('gamepage.html',success=success,game=game,streamer=streamName,users=users, username=username)

@app.route('/wishlist/<gameid>', methods=['POST'])
def changeWishlist(gameid):
    user = session['Username']
    if request.form["action"] == "Add to Wishlist":
        wishlist.addWishlist(user,gameid)
    elif request.form["action"] == "Remove from Wishlist":
        wishlist.removeWishlist(user,gameid)
    return redirect(url_for('gamepage',gameid=gameid))

    
@app.route('/twitch/')
def twitch():
    if 'token' in session:
        return redirect(url_for('homepage',error="You are already connected to Twitch"))  
    if 'Username' in session:
        keys = twitch_api.keys()
        return redirect('https://api.twitch.tv/kraken/oauth2/authorize?response_type=code&client_id=%s&redirect_uri=http://127.0.0.1:5000/&scope=chat_login'%(keys[0]))
    else:
        return redirect(url_for('homepage',error="You must log in first"))

@app.route("/logout/")
def logout():
    if "Username" in session:# can only log out if you are already logged in
        session.pop("Username")

    if "token" in session:# log out twitch token
        session.pop("token")
    return redirect (url_for('homepage',success="Logged out"))

if __name__ == '__main__':
    if os.path.getsize("data/database.db") == 0:
        f = "data/database.db"
        db = sqlite3.connect(f, check_same_thread=False)
        c = db.cursor()
        print "Initializing database"
        c.execute("CREATE TABLE users (username TEXT, password TEXT)")
        c.execute("CREATE TABLE wishlist (username TEXT, game INTEGER)")
        db.commit()
        db.close()
    app.debug=True
    app.secret_key = '  \x43\xd2\x34\x92\x5b\x4a\x80\xfc\xc6\xb0\x0e\x45\xdd\x51\x36\xc0\xd2\x3a\x85\x42\x57\xbb\x61\xf2\x7b\xb6\xfc\x17\x3b\x1a\xda\x5b\x6d\x7d\x0a\xff\xd3\x6f\xfa\x7c\x1b\xa8\x0f\x7f\x53\x18\x8d\x91\x16\x81'
    app.jinja_env.globals.update(inWishlist=wishlist.inWishlist)
    app.run()
