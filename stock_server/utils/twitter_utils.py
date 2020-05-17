import tweepy
from textblob import TextBlob

import stock_server.utils.constants as ct


class Tweet:
    def __init__(self, tw, polarity):
        self.tw = tw
        self.polarity = polarity


def get_polarity(symbol):
    auth = tweepy.OAuthHandler(ct.consumer_key, ct.consumer_secret)
    auth.set_access_token(ct.access_token, ct.access_token_secret)
    user = tweepy.API(auth)

    tweets = tweepy.Cursor(user.search, q=str(symbol), tweet_mode='extended', lang='en').items(ct.num_of_tweets)

    tweet_list = []
    positive = 0
    negative = 0
    global_polarity = 0
    for tweet in tweets:
        tw = tweet.full_text
        blob = TextBlob(tw)
        polarity = 0
        for sentence in blob.sentences:
            polarity += sentence.sentiment.polarity
        polarity /= len(blob.sentences)
        global_polarity += polarity
        if polarity > 0:
            positive += 1
        else:
            negative += 1
        tweet_list.append(Tweet(tw, polarity))

    global_polarity = global_polarity / len(tweet_list)
    return global_polarity
