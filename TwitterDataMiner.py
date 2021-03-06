# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 15:47:47 2021

@author: Roland
"""

import tweepy as tw
import pandas as pd
import json
import os

# Define path to the credentials
path_to_credentials = os.path.join(os.getcwd(), "credentials.json")
# Load the credentials 
with open(path_to_credentials) as file:
    credentials = json.load(file)

# Creating the authentication object
auth = tw.OAuthHandler(credentials["consumer_key"], credentials["consumer_secret"])

# Setting your access token and secret, uncomment the line below if you need the access token as well
auth.set_access_token(credentials["access_token"], credentials["access_token_secret"])

# Creating the API object while passing in auth information
api = tw.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

# The search term you want to finds
query = 'covid vaccine'
start_date = '2021-03-02'
end_date = '2021-03-03' # excluding the date
max_tweets = 900 # 900 is the rate limit set by Twitter per 15 minutes
geocode = '12.8797,121.7740,500mi' # Center of the Philippines geocode
last_id = '' # leave blank if none

# Calling the user_timeline function with our parameters
results = tw.Cursor(api.search, q=query,  since=start_date, until=end_date, 
                    tweet_mode='extended', geocode=geocode, max_id=last_id).items(max_tweets)

tweets_list = [[tweet.id_str, tweet.created_at, tweet.full_text, tweet.lang, 
                tweet.retweet_count, tweet.favorite_count, 
                tweet.entities, tweet.in_reply_to_screen_name, 
                tweet.in_reply_to_status_id_str, tweet.in_reply_to_user_id_str, 
                tweet.source, tweet.user.id_str, tweet.user.name, tweet.user.screen_name, 
                tweet.user.description, tweet.user.location, 
                tweet.user.followers_count, tweet.user.friends_count] 
               for tweet in results]
 
c = ['id_str','created_at','full_text','lang','retweet_count',
     'favorite_count','entities','in_reply_to_screen_name','in_reply_to_user_id_str',
     'in_reply_to_user_id_str','source','user.id_str','user.name','user.screen_name',
     'user.description','user.location','user.followers_count','user.friends_count']

# Creation of dataframe from tweets_list
tweets_df = pd.DataFrame(tweets_list, columns=c)

# Save dataframe to csv
FilePath = start_date + last_id + '.csv'
tweets_df.to_csv(FilePath,index=False)