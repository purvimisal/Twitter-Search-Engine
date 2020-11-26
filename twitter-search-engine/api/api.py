import time
import json
from flask import Flask,Response,request
from pymongo import MongoClient
import pprint
from bson.objectid import ObjectId

app = Flask(__name__)
doc_collection = None
tweet_collection = None
MAX = 2000

@app.route('/')
def get_current_time():
    resp = {'time': time.time()}
    print(resp)
    return resp


#search text API
@app.route('/searchText',methods=['GET'])
def searchText():

    global doc_collection,tweet_collection
    json_body = request.get_json()

    words = json_body['text']
    words = words.lower()
    words = words.split(" ")
    docs_score = {}


    query = { "word":{"$in":words}}

    print('query : ' + str(query))
    datas = doc_collection.find(query)



    # calculating the tf-idf score for each document
    for data in datas:
        docs = data.get('docs')
        for doc in docs:
            if(doc.get('docId') not in docs_score):
                docs_score[str(doc.get('docId'))] = doc.get('score')
            else:
                docs_score[str(doc.get('docId'))] = docs_score[str(doc.get('docId'))] + doc.get('score')

    docs_score = dict(sorted(docs_score.items(), key=lambda item: item[1], reverse=True))
    final_query_list = list()



    #creating a list of Object(Key)

    index = 0
    for key in  docs_score.keys():
        if(index > MAX):
            break
        final_query_list.append(ObjectId(key))
        index += 1


    #query = { "_id":{"$in":final_list}}

    #finding the docs fro tweet collection
    print('query : ' + str(query))
    query = { "_id":{"$in":final_query_list}}
    #query = { "match":query}

    tweets = tweet_collection.find(query)
    #tweets = tweet_collection.aggregate([query])


    response = []

    #creating final object
    for i, tweet in enumerate(tweets):
        x = {}
        x['tweet'] = tweet
        x['score'] = docs_score[str(tweet['_id'])]
        response.append(x)


    response = (sorted(response, key=lambda x: -x['score']))
    #print('final response' + str(response))

    print(type(response))
    print(len(response))
    return Response(response = json.dumps(str(response)),status=200,content_type='Application/json')

#method to connect Db
def connectDb():
    global doc_collection,tweet_collection
    mongoclient = MongoClient(
        'mongodb+srv://cmpe297-user:cmpe297-user@project-cmpe297.2ylzz.mongodb.net/<twitterdb>?retryWrites=true&w=majority',
        ssl=True, ssl_cert_reqs='CERT_NONE')
    db = mongoclient['twitterdb']
    doc_collection = db['tweet_tf-idf_score']
    tweet_collection = db['twitter_collection']



connectDb()

