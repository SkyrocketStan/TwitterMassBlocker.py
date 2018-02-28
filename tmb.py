#!/usr/bin/env python3

from credentials import *
import tweepy
import sys

#Make a connection
def connect():
    print("Establishing a connection..")
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
            return sys.argv[1].strip("/@ ")
        except IndexError:
            print("Something wrong with the command line argument")
            return False

# Returns enemy ID
def get_enemy_ID(api, enemy_name):
    print("Checking the username..")
    try:
        id = api.get_user(enemy_name).id
    except tweepy.TweepError as e:
        try:
            print("Error. Code " + str(e.args[0][0]['code']) + ". " + e.args[0][0]['message'])
        except TypeError:
            print("Unexpected type error found: ", str(e))
        sys.exit()
    else:
        return id


# Returns enemy's followers
def get_followers(api, id):
    return api.followers_ids(id)

# Block the enemy by ID
def block_enemy(api, id):
    try:
        api.create_block(id)
    except tweepy.TweepError as e:
        try:
            print("Error. Code " + str(e.args[0][0]['code']) + ". " + e.args[0][0]['message'])
        except TypeError:
            print("Unexpected type error found: ", str(e))


# Mass blocking
def mass_blocking(api, id_list):
    for id in id_list:
        block_enemy(api, id)

# Get my friends list
def get_my_friends(api):
    return api.friends_ids()

# Make sure I do not block any of MY friends
def get_sorted_list_to_block(my_friends, enemy_followers):
    print("Calculating list to block..")
    sorted_ids = list(set(enemy_followers) - set(my_friends))
    return sorted_ids

# Clear list from any duplicates
def get_sorted_list(list_to_sort, clear_list):
    return list(set(list_to_sort) - set(clear_list))

# Get list my blocked IDs
def get_my_block_list(api):
    print("Getting MY blocked list..")
    return api.blocks_ids()['ids']

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
enemy_followers_count = len(enemy_followers)
print("Enemy's followers cout: " + str(enemy_followers_count))

# Get my friends and my block list
my_friends = get_my_friends(client)
my_blocked = get_my_block_list(client)
my_blocked_count = len(my_blocked)
print("My blocked counter: " + str(my_blocked_count))
# i do not want to block my friends
enemy_sorted_followers = get_sorted_list_to_block(my_friends, enemy_followers)

# Clear blocked list from ID's that is already blocked
enemy_followers_list = get_sorted_list(enemy_sorted_followers, my_blocked)

enemy_followers_sorted_count = len(enemy_followers_list)


print("Blocking the enemy..")
block_enemy(client, enemy_ID)

if enemy_followers_sorted_count > 0:
    # block'em all
    print("Sorted enemy's followers to block: " + str(enemy_followers_sorted_count))
    print("Let's block them all..")
    mass_blocking(client, enemy_sorted_followers)
else:
    print("No followers to block!")

print("Well done!")
