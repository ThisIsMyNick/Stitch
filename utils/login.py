#!/usr/bin/python

from hashlib import sha1
from sqlite3 import connect

f = "data/database.db"

def login(user, password):
    db = connect(f)
    c = db.cursor()
    query = ("SELECT * FROM users WHERE username=?")
    sel = c.execute(query,(user,));
    
    #records with this username
    #so should be at most one record (in theory)
     
    for record in sel:
        password = sha1(password).hexdigest()
        if (password==record[1]):
            return "" #no error message because it will be rerouted to mainpage
        else:
            return "Invalid password"#error message
    db.close()
    
    return "User does not exist"#error message

def register(user, password):
    db = connect(f)
    c = db.cursor()
    try: #does table already exist?
        c.execute("SELECT * FROM users")
    except: #if not, this is the first user!
        c.execute("CREATE TABLE users (username TEXT, password TEXT)")
    db.commit()
    db.close()
    return regMain(user, password)#register helper

def regMain(user, password):#register helper
    db = connect(f)
    c = db.cursor()
    reg = regReqs(user, password)
    if reg == "": #if error message is blank then theres no problem, update database
        query = ("INSERT INTO users VALUES (?, ?)")
        password = sha1(password).hexdigest()
        c.execute(query, (user, password))
        db.commit()
        db.close()
        return 1
    db.commit()
    db.close()
    return reg#return error message
        
def regReqs(user, password):      #error message generator
    if duplicate(user):          #checks if username already exists
        return "Username already exists"
    if " " in user:
        return "Spaces not allowed in username"
    return ""

def duplicate(user):#checks if username already exists
    db = connect(f)
    c = db.cursor()
    query = ("SELECT * FROM users WHERE username=?")
    sel = c.execute(query, (user,))
    retVal = False
    for record in sel:
        retVal = True
    db.commit()
    db.close()
    return retVal

   
#import os
#os.chdir('..')
#print(register("hello","world"))
#print(register("helloz","world"))
#print(login("helloz","world"))