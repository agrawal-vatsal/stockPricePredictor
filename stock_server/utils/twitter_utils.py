import tweepy
from textblob import TextBlob

import stock_server.utils.constants as ct
from _datetime import datetime


class Tweet:
    def __init__(self, tw, polarity):
        self.tw = tw
        self.polarity = polarity


def get_polarity(symbol):
    auth = tweepy.OAuthHandler(ct.consumer_key, ct.consumer_secret)
    auth.set_access_token(ct.access_token, ct.access_token_secret)
    user = tweepy.API(auth)
    tweets = tweepy.Cursor(user.search,
                           q=str(symbol),
                           tweet_mode='extended',
                           since=datetime.today().strftime('%Y-%m-%d'),
                           lang='en').items(ct.num_of_tweets)
    tweet_list = []
    global_polarity = 0
    for tweet in tweets:
        tw = tweet.full_text
        blob = TextBlob(tw)
        polarity = 0
        for sentence in blob.sentences:
            polarity += sentence.sentiment.polarity
        polarity /= len(blob.sentences)
        global_polarity += polarity
        tweet_list.append(Tweet(tw, polarity))

    global_polarity = global_polarity / len(tweet_list)
    return global_polarity
