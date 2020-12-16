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

# def jprint(obj):
#     # create a formatted string of the Python JSON object
#     text = json.dumps(obj, sort_keys=True, indent=4)
#     print(text)

def get_trending():

    try:
        trending_data_new = requests.get('https://api.coingecko.com/api/v3/search/trending')
        trending_coins_new = trending_data_new.json()['coins']

        trendinglist_name_new = []

    except requests.ConnectionError or requests.ConnectTimeout or requests.HTTPError or requests.NullHandler or requests.ReadTimeout or requests.RequestException or requests.RequestsDependencyWarning or requests.Timeout or requests.TooManyRedirects:
        print('There was an error...')

    for items in trending_coins_new:
        trending_name_new = items['item']['name'] + " $" + items['item']['symbol']
        trendinglist_name_new.append(trending_name_new)

    api = twitter_auth()
    client_id = api.me().id

    # Search for last tweet about trending coins
    if 'Currently Trending' in api.user_timeline(id=client_id, count=1, tweet_mode='extended')[0].full_text:
        tweet_text_1 = api.user_timeline(id=client_id, count=1, tweet_mode='extended')[0].full_text
        latest_tweet_topremove = tweet_text_1.split("\n", 3)[3]
        latest_tweet_trending = latest_tweet_topremove.rsplit("\n", 2)[0]
        last_trending_text = latest_tweet_trending.splitlines()
    elif 'Currently Trending' in api.user_timeline(id=client_id, count=2, tweet_mode='extended')[1].full_text:
        tweet_text_2 = api.user_timeline(id=client_id, count=2, tweet_mode='extended')[1].full_text
        latest_tweet_topremove = tweet_text_2.split("\n", 3)[3]
        latest_tweet_trending = latest_tweet_topremove.rsplit("\n", 2)[0]
        last_trending_text = latest_tweet_trending.splitlines()
    elif 'Currently Trending' in api.user_timeline(id=client_id, count=3, tweet_mode='extended')[2].full_text:
        tweet_text_3 = api.user_timeline(id=client_id, count=3, tweet_mode='extended')[2].full_text
        latest_tweet_topremove = tweet_text_3.split("\n", 3)[3]
        latest_tweet_trending = latest_tweet_topremove.rsplit("\n", 2)[0]
        last_trending_text = latest_tweet_trending.splitlines()
    elif 'Currently Trending' in api.user_timeline(id=client_id, count=4, tweet_mode='extended')[3].full_text:
        tweet_text_4 = api.user_timeline(id=client_id, count=4, tweet_mode='extended')[3].full_text
        latest_tweet_topremove = tweet_text_4.split("\n", 3)[3]
        latest_tweet_trending = latest_tweet_topremove.rsplit("\n", 2)[0]
        last_trending_text = latest_tweet_trending.splitlines()
    elif 'Currently Trending' in api.user_timeline(id=client_id, count=5, tweet_mode='extended')[4].full_text:
        tweet_text_5 = api.user_timeline(id=client_id, count=5, tweet_mode='extended')[4].full_text
        latest_tweet_topremove = tweet_text_5.split("\n", 3)[3]
        latest_tweet_trending = latest_tweet_topremove.rsplit("\n", 2)[0]
        last_trending_text = latest_tweet_trending.splitlines()
    else:
        print("Error can't find last trending tweet..")

    last_trending_list = []

    for item in last_trending_text:
        last_trending = item.strip()
        last_trending_list.append(last_trending)

    print(last_trending_list)
    print(trendinglist_name_new)

    if set(last_trending_list) == set(trendinglist_name_new):
        print("Nothing has changed...")
    elif set(last_trending_list) != set(trendinglist_name_new):
        trendinglist_difference = []
        for item in trendinglist_name_new:
            if item not in last_trending_list:
                trendinglist_difference.append(item)
        tweet_text_top = " entered trending on @coingecko! 🔥\n\n"
        tweet_var_top = '& '.join(trendinglist_difference)
        tweet_current_trending_text = "Currently Trending🚨:\n"
        tweet_trending = '\n'.join(trendinglist_name_new)
        tweet_text_bottom = "\n\n#bitcoin #crypto"
        api = twitter_auth()
        api.update_status(status=("🔥 " + tweet_var_top + tweet_text_top + tweet_current_trending_text + tweet_trending + tweet_text_bottom))
        print("🔥 ", tweet_var_top, tweet_text_top, tweet_current_trending_text, tweet_trending, tweet_text_bottom)
        trendinglist_difference.clear()
    else:
        print("An error has occurred...")
        
def like_tweets():
    api = twitter_auth()
    max_tweets = 5
    for tweet in tweepy.Cursor(api.search, q='#bitcoin', count=5, result_type="recent").items(max_tweets):
        try:
            print(f"Liking tweet {tweet.id} of {tweet.author.name}")
            api.create_favorite(tweet.id)
        except:
            print("Tweets already liked")
    for tweet in tweepy.Cursor(api.search, q='#crypto', count=5, result_type="recent").items(max_tweets):
        try:
            print(f"Liking tweet {tweet.id} of {tweet.author.name}")
            api.create_favorite(tweet.id)
        except:
            print("Tweets already liked")
            
get_trending()
like_tweets()




