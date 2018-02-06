#!/usr/bin/env python3

# Import our Twitter credentials from credentials.py
import tweepy
from time import sleep
from credentials import *

# Access and authorize our Twitter credentials from credentials.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Write a tweet to push to our Twitter account
tweet = 'Hello, world!'
api.update_status(status=tweet)