import tweepy
import os 
import keyring
import pandas as pd
import numpy as np
import string 
import time
from sqlalchemy import create_engine
import psycopg2

# import helpers as pj

# Helper functions 
# from helpers import import_tweets_to_db
# from helpers import get_last_tweet_id
# from helpers import loop_tweets
exec(open(os.path.join('.','Python','helpers.py'), encoding="utf8").read())


# Pull in Passwords
exec(open(os.path.join('.','consumerpy')).read())

# Open the Connection to Twitter
auth = tweepy.OAuthHandler(keyring.get_password('cov_gov','TWITTER_KEY'),keyring.get_password('cov_gov','TWITTER_SECRET'))
auth.set_access_token(keyring.get_password('cov_gov','TWITTER_TOKEN'), keyring.get_password('cov_gov','TWITTER_TOKEN_SEC'))
api = tweepy.API(auth,wait_on_rate_limit=True,retry_count=20,retry_delay=10,retry_errors=[401, 404, 500, 503],wait_on_rate_limit_notify=True)


g = pd.read_csv('govlist.csv').fillna('')
gov_list = g.twitter_handle.to_list() + g[g.personal_twitter != ''].personal_twitter.to_list()

# for us in gov_list:
#    print(us)

# os.system('export DATABASE_URL=$(heroku config:get DATABASE_URL -a cov-gov-twitter)')
for user in gov_list:
    print(user)
    # get_oldest_tweet_id(screen_name= screen_name,db_str='postgres://127.0.0.1:5432/tt')
    # loop_tweets(screen_name=user, api= api, db_str = os.environ['DATABASE_URL'])
    loop_tweets(screen_name=user, api= api, csv_dir = 'db')
    # loop_tweets(screen_name=user, api= api, db_str = 'postgres://127.0.0.1:5432/tt')

