get_oldest_tweet_id(screen_name= 'BarackObama',db_str=db_str)

def loop_tweets(screen_name, db_str = 'postgres://127.0.0.1:5432/tt'):
    # Target Acquired
    username = screen_name
    user = api.get_user(username)

    # Get the tweets, 199 at a time
    last_id = get_oldest_tweet_id(screen_name= user.screen_name,db_str=db_str)
    for i in range(100):
        tweets = api.user_timeline(screen_name = user.screen_name, count=199, max_id = last_id, since_id = 1)
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
        print(last_id)



last_id = get_oldest_tweet_id(screen_name= user.screen_name,db_str=db_str)
tweets = api.user_timeline(screen_name = user.screen_name, count=2, max_id = None, since_id = 1)

# Open the Connection to Twitter
auth = tweepy.OAuthHandler(keyring.get_password('trumptweets','TWITTER_KEY'),keyring.get_password('trumptweets','TWITTER_SECRET'))
auth.set_access_token(keyring.get_password('trumptweets','TWITTER_TOKEN'), keyring.get_password('trumptweets','TWITTER_TOKEN_SEC'))
api = tweepy.API(auth)
#find things
tweets = api.search('plandemic',count=100)
df = pd.DataFrame({
    'id'        : [str(tweet.id) for tweet in tweets],
    'text'      : [tweet.text for tweet in tweets],
    'dttm'      : [tweet.created_at for tweet in tweets],
    'isRetweet' : [tweet.text[0:2] == 'RT' for tweet in tweets],
    'tweeter'   : [tweet.user.screen_name for tweet in tweets]
})
df.head()
df.shape