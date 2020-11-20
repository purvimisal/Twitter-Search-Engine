import time
from tweepy import Stream
from tweepy import OAuthHandler
import tweepy
from tweepy.streaming import StreamListener
import io
import os
import json
from pymongo import MongoClient

consumer_key = ''
consumer_secret = ''
access_token_key = ''
access_token_secret = ''

class Streamlistener(tweepy.StreamListener):
    def __init__(self, api=None):
        super().__init__(api=api)
        self.counter = 0
        self.tweet_data = []


    def on_connect(self):
        print("You are connected to the Twitter API")

    def on_error(self, status_code):
        if status_code != 200:
            print("error found")
            # returning false disconnects the stream
            return False
    
    def on_data(self, data):
        try:
            saveFile = io.open('raw_tweets.json', 'w', encoding='utf-8')
            
            if self.counter == 100_000:
                return
            self.counter += 1
            try:
                self.tweet_data.append(data)
                # print('INSERTED!!')
            except BaseException as e:
                print('Error storing into collection', e)
            
            saveFile = io.open('raw_tweets.json', 'a+', encoding='utf-8')
            saveFile.write(','.join(self.tweet_data))
            saveFile.close()
            return True 



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
    track = ['cricket', 'ipl', 'India vs Australia', 'BCCI', 'Sourav Ganguly', 'Virat kohli', 'Espn', 'cricInfo', 'cricBuzz', 'IPL2020', 'ICC', 'SportsCenter', 'Rohit Sharma', 'Sachin', 'BigBash']
    
    stream.filter(track = track,languages = ['en'])
    