#!/usr/bin/env python3

import tweepy
from creds import consumer_key, consumer_secret, access_token, access_token_secret
from random import sample
from time import sleep
from html import unescape

# --- get terms --- #
selector_terms = set(map(lambda x: x.strip('\n'), open('terms.txt','r').readlines()))

# --- set up API --- #
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# --- search for tweets containing a random selector term --- #
def retweet_selector(selector):
    # grab a tweet containing this term
    search = " OR ".join(selector)
    tweet = api.search(q=search, lang='en').pop()
    print("Selectors:", ", ".join(selector))
    if any(x in tweet.user.screen_name for x in selector):
        print("Selector was in @" + tweet.user.screen_name)
        sleep(30)
        retweet_selector(selector)
    else:
        print('Retweeting', '\"' + unescape(tweet.text) + '\" from @'+tweet.user.screen_name)
        # retweet it
        #api.retweet(tweet.id)

# --- main etc ? --- #
while True:
    selector = sample(selector_terms, 8)
    try:
        retweet_selector(selector)
        sleep(15 * 60)
    except tweepy.error.TweepError as e:
        print(e)
        sleep(15 * 60)
    except Exception as e:
        print(e)
        raise

