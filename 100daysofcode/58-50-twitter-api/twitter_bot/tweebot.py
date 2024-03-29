import datetime
import logging
import sys
import time

import feedparser
import tweepy

from config import LOGFILE, HASHTAG
from config import CONSUMER_KEY, CONSUMER_SECRET
from config import ACCESS_TOKEN, ACCESS_SECRET


FEEDS = 'feeds'
MAX_ENTRIES = 5
NOW = time.localtime()
NOW_UTSTAMP = time.mktime(NOW)
NOW_READABLE = datetime.datetime.fromtimestamp(
        int(NOW_UTSTAMP)
    ).strftime('%Y-%m-%d %H:%M:%S')
PYBITES = 'pybit.es'
SECONDS_IN_DAY = 24 * 60 * 60

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%H:%M:%S',
                    filename=LOGFILE,
                    filemode='a')

class TwitterApi(object):

    def __init__(self):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        self.api = tweepy.API(auth)
        logging.debug(f"Created {self.__class__.__name__} instance")

    def post_tweet(self, status):
        try:
            self.api.update_status(status)
            logging.debug(f"posted status {status} to twitter")
        except Exception as exc:
            logging.error(f"tweepy update_status error: {exc}")


def get_feeds():
    with open(FEEDS) as f:
        return f.read().split()

def within_last_day(tstamp):
    return (time.mktime(NOW) - time.mktime(tstamp)) / SECONDS_IN_DAY < 1

def create_tweet(entry):
    return " ".join([entry['title'], entry['link'], HASHTAG])

def get_tweets(feed):
    for entry in feedparser.parse(feed)['entries'][:MAX_ENTRIES]:
        tstamp = entry['published_parsed']
        if within_last_day(tstamp):
            yield create_tweet(entry)

if __name__ == '__main__':
    logging.debug(f"New run at {NOW_READABLE}, processing feeds")

    do_tweet = True
    if '-d' in sys.argv:
        do_tweet = False

    twapi = TwitterApi()
    for feed in get_feeds():
        logging.debug(f"- feed: {feed}")

        for tweet in get_tweets(feed):
            logging.debug(tweet)
            print(tweet)
            if do_tweet:
                twapi.post_tweet(tweet)
