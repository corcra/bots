#!/usr/bin/env python3

import tweepy
from creds import consumer_key, consumer_secret, access_token, access_token_secret
from random import sample
from time import sleep
from html import unescape
import re

# --- get terms --- #
selector_terms = set(map(lambda x: x.strip('\n'), open('terms.txt','r').readlines()))

# --- set up API --- #
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def criteria(selector, tweet):
    if ("RT" in tweet.text) or ("t.co" in tweet.text):
        return False
    for element in selector:
        if (element in tweet.user.screen_name.lower() or
            re.search("@[a-zA-Z0-9_]*" + element + "[a-zA-Z0-9_]*", tweet.text.lower())):
            # don't use tweets selected by a handle
            return False
    return True

# --- search for tweets containing a random selector term --- #
def retweet_selector(selector):
    # grab a tweet containing this term
    search = " OR ".join(selector)
    tweet = api.search(q=search, lang='en').pop()
    if criteria(selector, tweet):
        print("Selectors:", ", ".join(selector))
        print('Retweeting', '\"' + unescape(tweet.text) + '\" from @' + tweet.user.screen_name)
        # retweet it
        api.retweet(tweet.id)
        sleep(60 * 60)

# --- main etc ? --- #
while True:
    selector = sample(selector_terms, 8)
    try:
        retweet_selector(selector)
    except tweepy.error.TweepError as e:
        print(e)
        sleep(15 * 60)
    except IndexError as e:  # in case the search results list is empty
        print("IndexError:", e)
        sleep(15)
    except Exception as e:
        print(e)
        raise

