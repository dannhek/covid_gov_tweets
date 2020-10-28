import tweepy
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import string 
import time
import re
import urllib.request as urllib2
import urllib.parse as urlp


###############################################################
#####################  Categorizers  ##########################
###############################################################
# Identify if the tweet is about COVID
def tweet_about_covid(tweet_str):
    ret = False
    covid_words = [
        'covid',
        'covid19',
        'sars',
        'sarscov2',
        'sarscov',
        'wuhan',
        'coronavirus',
        'virus',
        'pandemic'
    ]
    for word in tweet_str.split():
        if word.translate(word.maketrans('','',string.punctuation)).lower() in covid_words:
            ret = True
            break
    return ret

def categorize_url_domain(domains):
    ret = []
    for domain in domains:
        if domain in ['abc.com','cbs.com','foxnews.com','cnn.com','bbc.com','nytimes.com','bloomberg.com']:
            ret.append('Mainstream News')
        #
        elif domain in ['cdc.gov','who.int','nejm.org']:
            ret.append('Scientific Source')
        #
        elif re.match('.+\.gov.*',domain):
            ret.append('Government')
        #
        elif domain in ['media.twitter.com','twitter.com','amp.twimg.com']:
            ret.append('Twitter')
        #
        else:
            ret.append('Uncategorized')
    return ret


###############################################################
#####################  URL Handling  ##########################
###############################################################
def find_urls(text): 
    ret = []
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    urls = re.findall(regex,text)   
    for match in urls:   
        for url in list(match):
            if url == '':
                continue
            try:
                response = urllib2.urlopen(url) 
            except:
                continue
            if response.code == 200:
                if re.match('^https://twitter.com/i/web/status/',response.url):
                    #Ignore the link to the status itself
                    continue
                else:
                    ret.append(response.url)
    return ret


def extract_domains(urls):
    ret = []
    for url in urls:
        domain = re.sub('^www\.','',urlp.urlparse(url).netloc)
        ret.append(domain)
    return ret



def get_full_tweet_text(status):
    if hasattr(status, "retweeted_status"):  # Check if Retweet
        try:
            return status.retweeted_status.full_text
        except AttributeError:
            return status.text
    else:
        try:
            return status.full_text
        except AttributeError:
            return status.text


###############################################################
#################  Core Tweet Procesing  ######################
###############################################################
# Function to populate data model
def import_tweets_to_db(tweets, db_str):
    eng = create_engine(db_str)
    df = pd.DataFrame({
        'id'            : [str(tweet.id) for tweet in tweets],
        'text'          : [get_full_tweet_text(tweet) for tweet in tweets],
        'dttm'          : [tweet.created_at for tweet in tweets],
        'isRetweet'     : [tweet.text[0:2] == 'RT' for tweet in tweets],
        'tweeter'       : [tweet.user.screen_name for tweet in tweets],
        'covid_related' : [tweet_about_covid(tweet.text) for tweet in tweets],
    })
    df.to_sql('tweets', con = eng, if_exists='append', index=False)
    print(df.shape)
    for tweet in tweets:
        tokens = [s.rstrip(string.punctuation) for s in tweet.text.replace('\n',' ').split(' ')]
        hashtags = list(filter(lambda k: k.startswith('#'), tokens))
        userrefs = list(filter(lambda k: k.startswith('@'), tokens))
        urlrefs  = find_urls(tweet.text)
        if (len(hashtags) > 0) :
            h = {
            'tweet_id' : np.repeat(str(tweet.id),len(hashtags)),
            'line'     : list(range(max(len(hashtags),0))),
            'hashtag'  : hashtags
            }
            pd.DataFrame(h).to_sql('hashtags',con = eng,if_exists='append',index=False)
        if (len(userrefs) > 0) :
            u = {
            'tweet_id' : np.repeat(str(tweet.id),len(userrefs)),
            'line'     : list(range(max(len(userrefs),0))),
            'users'    : userrefs
            }
            pd.DataFrame(u).to_sql('atusers',con = eng,if_exists='append',index=False)
        if (len(urlrefs) > 0) :
            u = {
            'tweet_id' : np.repeat(str(tweet.id),len(urlrefs)),
            'line'     : list(range(max(len(urlrefs),0))),
            'url'      : urlrefs,
            'domain'   : extract_domains(urlrefs),
            'category' : (categorize_url_domain(extract_domains(url)) for url in urlrefs)
            }
            pd.DataFrame(u).to_sql('urlrefs',con = eng,if_exists='append',index=False)


# Get the last tweet ID for this user from the database. 
def get_oldest_tweet_id(screen_name, db_str):
    eng = create_engine(db_str)
    try: 
        tweet_id = pd.read_sql(sql="select id from tweets where tweeter = '{}' order by dttm limit 1".format(screen_name), con=eng)
        ret = int(tweet_id.iloc[0]['id']) - 1 
    except:
        ret = None
    return ret


def loop_tweets(screen_name, api, db_str):
    # Target Acquired
    username = screen_name
    user = api.get_user(username)
    # Get the tweets, 199 at a time
    last_id = get_oldest_tweet_id(screen_name= user.screen_name,db_str=db_str)
    for i in range(100):
        tweets = api.user_timeline(screen_name = user.screen_name, count=199, max_id = last_id, since_id = 1) #, tweet_mode = 'extended')
        ids = [tweet.id for tweet in tweets]
        if (len(ids)==0):
            #Made it through Everything... or something bombed
            print('Empty')
            break
        if (min(ids)==last_id):
            #Pulled the same thing again
            print('Same Last ID')
            break
        last_id = min(ids)-1
        print('{}: {}'.format(i,last_id))
        import_tweets_to_db(tweets = tweets, db_str = db_str)

