import sqlite3

def lenient(game):
    game = game.replace(" ", "%")
    game = game.replace("-", "%")
    game = game.replace(":", "%")
    game = "%" + game + "%"
    return game

def get_id(game):
    game = lenient(game)
    db = sqlite3.connect("data/app_ids.db")
    c = db.cursor()
    c.execute('SELECT * FROM apps WHERE name LIKE ?', (game,))
    g_id = c.fetchall()
    db.close()
    return g_id
