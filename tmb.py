#!/usr/bin/env python3

from credentials import *
import tweepy
import sys

#Make a connection
def connect():
    print("Connecting..")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

# get my own ID
def get_my_id(api):
    return api.me().id

# Get start argument
def get_enemy_name():
    '''Returns start argument or False if argument index does not exists'''
    if len(sys.argv) != 2:
        sys.exit("USAGE: " + sys.argv[0] + " <twitter_username> without @ sign")
    else:
        try:
            return sys.argv[1]
        except IndexError:
            print("Something wrong with the command line argument")
            return False

# Returns enemy ID
def get_enemy_ID(api, enemy_name):
    return api.get_user(enemy_name).id

# Returns enemy's followers
def get_followers(api, id):
    return api.followers_ids(id)

# Block the enemy by ID
def block_enemy(api, id):
    block_response = api.create_block(id) # response variable is for future using

# Mass blocking
def mass_blocking(api, id_list):
    for id in id_list:
        block_enemy(api, id)

# At first take the enemy's name. Otherwise no sense to establish connection
enemy_name = get_enemy_name()
#Establish connection
client = connect()
# Getting my OWN ID
my_ID = get_my_id(client)
# Get enemy's ID
enemy_ID = get_enemy_ID(client, enemy_name)
# Get enemy's followers
enemy_followers = get_followers(client, enemy_ID)
print('Enemy followers cout: ' + str(len(enemy_followers)))

# block'em all
block_enemy(client, enemy_ID)
mass_blocking(client, enemy_followers)

print("Well done")
