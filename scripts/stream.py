import time
from tweepy import Stream
from tweepy import OAuthHandler
import tweepy
from tweepy.streaming import StreamListener
import io
import os
import json
from pymongo import MongoClient



class Streamlistener(tweepy.StreamListener):
    def __init__(self, api=None):
        super().__init__(api=api)
        self.tweet_data = []

    def on_connect(self):
        print("You are connected to the Twitter API")

    def on_error(self, status_code):
        if status_code != 200:
            print("error found")
            # returning false disconnects the stream
            return False
    
    def on_data(self, data):
        # saveFile = io.open('raw_tweets.json', 'a', encoding='utf-8')
        try:
            self.tweet_data.append(data)
            mongoclient = MongoClient('mongodb://user:user@localhost:27017')

            try:
                db = mongoclient['twitterdb']
                collection = db['twitter_collection']
                tweet = json.loads(data)
                collection.insert(tweet)
                print('INSERTED!!')
                return True 
            except BaseException as e:
                print('Error storing into collection', e)

        except BaseException as e:
            print ('failed ondata,', str(e))
            time.sleep(5)
            pass
        
    def on_disconnect(self, notice):
        print('Bye!')

        


if __name__ == '__main__':

    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)

    api = tweepy.API(auth,wait_on_rate_limit=True)
    listener = Streamlistener(api =api)
    stream = tweepy.Stream(auth, listener = listener)
    track = ['cricket']
    
    stream.filter(track = track,languages = ['en'])