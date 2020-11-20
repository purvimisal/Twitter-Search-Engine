import io
import os
import json
from pymongo import MongoClient



json_file = io.open('raw_tweets.json', 'r', encoding='utf-8')

tweet_dictionary = json.load(json_file)
mongoclient = MongoClient('')
db = mongoclient['twitterdb']
collection = db['twitter_collection']


for tweet in tweet_dictionary[5:]:
    tweetdata = {}
    tweetdata['id'] = tweet['id']
    tweetdata['text'] = tweet['text']
    tweetdata['created_at'] = tweet['created_at']
    tweetdata['user_screen_name'] = tweet['user']['screen_name']
    tweetdata['user_name'] = tweet['user']['name']
    tweetdata['user_location'] = tweet['user']['location']
    tweetdata['user_description'] = tweet['user']['description']
    tweetdata['geo'] = tweet['geo']
    tweetdata['coordinates'] = tweet['coordinates']
    tweetdata['place'] = tweet['place']
    tweetdata['lang'] = tweet['lang']
    tweetdata['entities'] = tweet['entities']
    tweetdata['retweet_count'] = tweet['retweet_count']
    tweetdata['reply_count'] = tweet['reply_count']
    tweetdata['quote_count'] = tweet['quote_count']
    collection.insert(tweetdata)

print('DONE!!')
