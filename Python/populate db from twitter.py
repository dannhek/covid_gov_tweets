import tweepy
import os 
import keyring
import pandas as pd
import numpy as np
import string 
import time
from sqlalchemy import create_engine
import psycopg2

import helpers as pj

# Helper functions 
# from helpers import import_tweets_to_db
# from helpers import get_last_tweet_id
# from helpers import loop_tweets
# exec(open('helpers.py').read())


# Pull in Passwords
exec(open('./consumerpy').read())

# Open the Connection to Twitter
auth = tweepy.OAuthHandler(keyring.get_password('trumptweets','TWITTER_KEY'),keyring.get_password('trumptweets','TWITTER_SECRET'))
auth.set_access_token(keyring.get_password('trumptweets','TWITTER_TOKEN'), keyring.get_password('trumptweets','TWITTER_TOKEN_SEC'))
api = tweepy.API(auth,wait_on_rate_limit=True,retry_count=20,retry_delay=10,retry_errors=[401, 404, 500, 503],wait_on_rate_limit_notify=True)

screen_name = 'GovAbbott'
# get_oldest_tweet_id(screen_name= screen_name,db_str='postgres://127.0.0.1:5432/tt')
loop_tweets(screen_name=screen_name, api= api)

