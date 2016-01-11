#!/usr/bin/env python3
# this is mostly a clone of XKS

import tweepy
from creds import consumer_key, consumer_secret, access_token, access_token_secret
import re
from random import choice

verbose = True

def badtweet(tweet):
    """
    Hand-crafted criteria.
    """
    if tweet.text[:2] == 'RT':
        return True
    if not 'NASA' in tweet.text:
        return True
    if '@NASA' in tweet.text:
        return True
    if tweet.text[0] == '@':
        return True
    return False

# --- set up API --- #
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if verbose: print 'authed, searching'

# --- find a tweet --- #
tweets = api.search(q="NASA -@NASA -http", lang="en")

if verbose: print 'tweets found, picking a good one...'

# ... pick a good one
tweet = choice(tweets)
while badtweet(tweet):
    tweet = choice(tweets)
print tweet.text

# --- find/replace --- #
NASA_tweet = re.sub("NASA", "NSA", tweet.text)
print NASA_tweet

# --- post --- #
api.update_status(status=NASA_tweet)
