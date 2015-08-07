#!/bin/python

import tweepy
from numpy import load
from creds import consumer_key, consumer_secret, access_token, access_token_secret

selector_terms = load('terms.npy').item()

# --- get set up API --- #
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_torkn(access_token, access_token_secret)
api = tweepy.API(auth)

# --- ... things ... --- #
