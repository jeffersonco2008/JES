from twython import Twython

KEY = "Your Key Here"
KEY_SECRET = "Your Key Here" 
ACCESS_TOKEN = "Your Key Here"
ACCESS_TOKEN_SECRET = "Your Key Here"

t = Twython(app_key=KEY, 
            app_secret=KEY_SECRET, 
            oauth_token=ACCESS_TOKEN, 
            oauth_token_secret=ACCESS_TOKEN_SECRET)
