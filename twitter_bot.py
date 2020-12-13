import tweepy
import time
import datetime
import os
from os import environ
import requests
from pycoingecko import CoinGeckoAPI
import json
import pickle

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']


def twitter_auth():
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    # Create API object
    api = tweepy.API(auth)
    # Test twitter credentials
    try:
        api.verify_credentials()
        print("Authenticated OK")
    except:
        print("Error during authentication")
    return api


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def get_initial_trending():
    # get initial trending coin data and store in trendinglist
    trending_data = requests.get('https://api.coingecko.com/api/v3/search/trending')
    trending_coins = trending_data.json()['coins']

    trendinglist_name = []

    for items in trending_coins:
        trending_name = items['item']['name'] + " $" + items['item']['symbol']
        trendinglist_name.append(trending_name)

    with open('trendfile.txt', 'wb') as trendfile:
        pickle.dump(trendinglist_name, trendfile)


def get_trending():
    with open('trendfile.txt', 'rb') as trendfile:
        trendinglist_name = pickle.load(trendfile)

    print(trendinglist_name)

    # infinite loop, get new trending data, compare to old trending data and print/tweet any new items
    # while True:
    try:
        trending_data_new = requests.get('https://api.coingecko.com/api/v3/search/trending')
        trending_coins_new = trending_data_new.json()['coins']

        trendinglist_name_new = []

    except requests.ConnectionError or requests.ConnectTimeout or requests.HTTPError or requests.NullHandler or requests.ReadTimeout or requests.RequestException or requests.RequestsDependencyWarning or requests.Timeout or requests.TooManyRedirects:
        print('There was an error...')

    for items in trending_coins_new:
        trending_name_new = items['item']['name'] + " $" + items['item']['symbol']
        trendinglist_name_new.append(trending_name_new)

    trendinglist_difference = []

    if set(trendinglist_name) == set(trendinglist_name_new):
        print("Nothing has changed...")
    elif set(trendinglist_name) != set(trendinglist_name_new):
        for item in trendinglist_name_new:
            if item not in trendinglist_name:
                trendinglist_difference.append(item)
        tweet_text_top = "🔥A new coin has just entered trending on @coingecko!🔥\n\n"
        tweet_var = '\n'.join(trendinglist_difference)
        tweet_text_bottom = "\n\n#cryptocurrency #bitcoin #crypto"
        api = twitter_auth()
        api.update_status(tweet_text_top + tweet_var + tweet_text_bottom)
        print(tweet_text_top, tweet_var, tweet_text_bottom)
        trendinglist_difference.clear()
        with open('trendfile.txt', 'wb') as trendfile:
            pickle.dump(trendinglist_name_new, trendfile)
    else:
        print("An error has occurred...")

    # time.sleep(60*30)

get_trending()



