import time
import json
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app)

doc_collection = None
tweet_collection = None
MAX = 500

@app.route('/')
def get_current_time():
    resp = {'time': time.time()}
    print(resp)
    return resp


#search text API
@app.route('/searchText',methods=['POST'])
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
    #json_list = []
    #for res in response:
    #    json_obj = {'doc_info':res}
     #   json_list.append(json.dumps(json_obj))


    json_data = json.loads(dumps(response))
    return jsonify({'data': json_data })


#search fields API
@app.route('/searchFields',methods=['POST'])
def search_fields():
    global doc_collection,tweet_collection

    ''' 
    Request Object:
    {
        "user_name": "",
        "user_location": "",
        "user_mention":"",
        "hashtag": "",
    }
    '''
    json_body = request.get_json()
    query = {}
    field_count = 0
    if json_body['user_name']:
        field_count += 1
        query['user_name'] = json_body['user_name'] 
    
    if json_body['user_location']:
        field_count += 1
        query['user_location'] = json_body['user_location']
    
    # if json_body['user_description']:
    #     field_count += 1
    #     query['$text'] = { "$search": json_body['user_description']}
    
    if json_body['user_mention']:
        field_count += 1
        query['entitities.user_mentions.name'] =  json_body['user_mention'] 
    
    if json_body['hashtag']:
        field_count += 1
        query['entities.hashtags.text'] = json_body['hashtag']
    
    if field_count == 0:
        return jsonify({'error': 'Please fill at least one query field'})
    
    filter_list = []
    for key, val in query.items():
        filter_list.append({key:val})

    and_query = {"$and" : filter_list}
    response_and = list(tweet_collection.find(and_query))
    if field_count == 1 or len(response_and)>=MAX: 
        response = json.loads(dumps(response_and))
        return jsonify(response)
    elif len(response_and) == 0:
        or_query = {"$or" : filter_list}
        response_or = list(tweet_collection.find(or_query).limit(MAX))
        response = json.loads(dumps(response_or))
        return jsonify(response)
    else:
        lim = MAX-len(response_and)
        or_query = {"$or" : filter_list}
        response_or = list(tweet_collection.find(or_query).limit(lim))
        if len(response_and) == len(response_or):
            response = json.loads(dumps(response_or))
            return jsonify(response)

    response = response_and.copy()
    for obj in response_or:
        if obj not in response_and:
            response.append(obj)

    response = json.loads(dumps(response))
    return jsonify(response)
    

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
