#Stitch#
-----
A sleek gamehub that connects your favorite games on steam and twitch. Track your favorite games and when they go on sale, and follow your favorite games on twitch. Learn who else shares your fine taste in games, and check out their wishlists too. 
-----
##Requires:##

* sqlite3 
* flask

And that's it!
-----
##Using the site
The site lists games that are on the Steam Featured page. 
####Gamepage
Clicking on a game will lead to the gamepage, where you can view the most popular live Twitch stream for that game.

If you are logged in, the gamepage will allow you to add a game to your wishlist. You can also view other people who have favorited the game, and visit their profiles.



Notes:
We also used the *lxml* library to generate an app_id database from steamdb.info. 
Since the steam api does not include a list of all steam games, we had to parse info from steamdb.info to implement a search function.






