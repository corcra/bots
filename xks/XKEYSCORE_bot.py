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

def criteria(selector, tweet):
    if ("RT" in tweet.text) or ("t.co" in tweet.text):
        return False
    for element in selector:
        if element in tweet.user.screen_name.lower():  # don't select based
            return False                               # on handle
        if tweet.entities.get("user_mentions"):
            for mention in tweet.entities.get("user_mentions"):
                if element in mention["screen_name"].lower():
                    return False
    return True

# --- search for tweets containing a random selector term --- #
def retweet_selector(selector):
    # grab a tweet containing these terms
    search = " OR ".join(selector)
    tweets = api.search(q=search, lang='en', count=100)
    tweets[:] = [tweet for tweet in tweets if criteria(selector, tweet)]
    tweet = tweets.pop(0)

    print("Selectors:", ", ".join(selector))
    print('Retweeting', '\"' + unescape(tweet.text) + '\" from @' + tweet.user.screen_name)

    # retweet it
    api.retweet(tweet.id)

# --- main etc ? --- #
while True:
    selector = sample(selector_terms, 8)
    try:
        retweet_selector(selector)
        sleep(60 * 60)
    except tweepy.error.TweepError as e:
        print(e)
        sleep(15 * 60)
    except IndexError:
        print("No results for", ", ".join(selector))  # in case the list of
        sleep(5)                                      # tweets is empty
    except Exception as e:
        print(e)
        raise

