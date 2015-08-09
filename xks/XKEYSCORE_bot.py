#!/bin/python

import tweepy
from numpy import load
from creds import consumer_key, consumer_secret, access_token, access_token_secret
from random import sample
from time import sleep

selector_terms = load('terms.npy').item()

# --- set up API --- #
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# --- search for tweets containing a random selector term --- #
def retweet_selector(selector):
    # grab a tweet containing this term
    tweet = api.search(q=selector, lang='en').pop()
    print 'Retweeting', tweet.text, 'from user', tweet.user.screen_name, 'because',
    print 'it contains selector term:', selector
    # retweet it
    api.retweet(tweet.id)


# --- main etc ? --- #
while True:
    selector = sample(selector_terms, 1)[0]
    retweet_selector(selector)
    sleep(15*60)
