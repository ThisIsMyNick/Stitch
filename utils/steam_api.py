import urllib2
import json

def parse_featured(s):
    d = json.loads(s)
    games = []
    for game in d['featured_win']:
        name = game['name']
        price = str(game['final_price'])
        price = price[:-2] + "." + price[-2:]
        discounted = game['discounted']
        discountpct = game['discount_percent']
        img = game['header_image']
        games.append((name,price,discounted,discountpct,img))
    return games

def get_featured():
    u = urllib2.urlopen("http://store.steampowered.com/api/featured")
    featured = parse_featured(u.read())
    return featured

def get_gamedata(gID):
    u = urllib2.urlopen("http://store.steampowered.com/api/appdetails/?appids=%s" % gID)
    d = json.loads(u.read())

    if d[str(gID)]['success'] == False:
        return

    data = d[str(gID)]['data']
    name = data['name']

    if data['is_free'] == True:
        price = 0
        discounted = False
        discount_percent = 0
    else:
        priceov = data['price_overview']
        price = priceov['final']
        if priceov['currency'] == "EUR":
            price *= 1.06
        price = str(price)
        price = price[:-2] + "." + price[-2:]
        if not priceov.get('discount_percent'):
            discountpct = 0
            discounted = False
        else:
            discountpct = priceov['discount_percent']
            discounted = False
            if discountpct != 0:
                discounted = True
    img = data['header_image']
    return (name,price,discounted,discountpct,img)
