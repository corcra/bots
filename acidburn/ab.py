#!/usr/bin/env python3
# this is mostly a clone of XKS

import tweepy
from creds import consumer_key, consumer_secret, access_token, access_token_secret

verbose = True

# --- set up API --- #
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

if verbose: print 'authed'

# --- get line --- #
line_number = int(open('ab_counter.txt', 'r').readline().strip('\n'))
for (number, line) in enumerate(open('hp.txt', 'r')):
    if number == line_number:
        print 'found line number', line_number
        print line
        hp_line = line.strip('\n')
        # post it
        #api.update_status(status=hp_line)
        break
line_number += 1
open('ab_counter.txt', 'w').write(str(line_number) + '\n')

