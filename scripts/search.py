import re
import pandas as pd
import string
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
import preprocessor as p
import numpy as np
import json
import csv
from gensim.parsing.preprocessing import remove_stopwords
#from bplustree import BPlusTree


def clean_documents(documents):
    documents_clean = []

    p.set_options(p.OPT.URL,p.OPT.EMOJI,p.OPT.SMILEY,p.OPT.NUMBER)
    for d in documents:
        # Remove Unicode
        d = d.lower()
        # removing url,emoji,smiley,number
        document_test = p.clean(d)

        #remove stop_words
        document_test = remove_stopwords(document_test)

        document_test = re.sub(r'[^\x00-\x7F]+', ' ', document_test)
        # Remove Mentions
        document_test = re.sub(r'@\w+', '', document_test)
        # Lowercase the document

        # Remove punctuations
        document_test = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', document_test)
        # Lowercase the numbers
        document_test = re.sub(r'[0-9]', '', document_test)
        # Remove the doubled space

        documents_clean.append(document_test)
    return documents_clean

def read_docs(filePath):
    df = pd.read_csv(filePath,delimiter=',')
    return df


def vectorize(docs,ids):
    # Instantiate a TfidfVectorizer object
    vectorizer = TfidfVectorizer()
    # It fits the data and transform it as a vector
    X = vectorizer.fit_transform(docs)
    # Convert the X as transposed matrix

    X = X.T.toarray()
    # Create a DataFrame and set the vocabulary as the index
    df = pd.DataFrame(X, index=vectorizer.get_feature_names(),columns=ids)
    return df,vectorizer.get_feature_names()

def indexing_word_docs(words,ids,docs,collection):
    word_list_final = list()

    for word in words:
        doc_list = list()
        print(word)
        for i in range(0, len(docs)):
            if word in docs[i] and df.loc[word][ids[i]] > 0.0:
                info = {'docId': ids[i], 'score': df.loc[word][ids[i]]}
                doc_list.append(info)
        obj = {'word': word, 'docs': doc_list}

        word_list_final.append(obj)
        try:
            collection.insert_one(obj)
        except Exception as e:
            print(word, 'Error occured', e)

    return word_list_final

def add_to_db(word_list_final):
    mongoclient = MongoClient('mongodb+srv://cmpe297-user:cmpe297-user@project-cmpe297.2ylzz.mongodb.net/<twitterdb>?retryWrites=true&w=majority',ssl=True,ssl_cert_reqs='CERT_NONE')
    db = mongoclient['twitterdb']
    collection = db['tweet_tf-idf_score']
    collection.insert_many(word_list_final)

def connectDb():
    mongoclient = MongoClient(
        'mongodb+srv://cmpe297-user:cmpe297-user@project-cmpe297.2ylzz.mongodb.net/<twitterdb>?retryWrites=true&w=majority',
        ssl=True, ssl_cert_reqs='CERT_NONE')
    db = mongoclient['twitterdb']
    collection = db['tweet_tf-idf_score']
    return collection

df = read_docs('data.csv')


print(df)
docs = df['text'].tolist()
ids = df['_id'].tolist()
#print(docs)

docs = clean_documents(docs)
print(docs)
def clean_tweets(docs):
    p.set_options(p.OPT.URL, p.OPT.EMOJI)




#docs = clean_tweets(docs)
print(type(docs))
df,words = vectorize(docs,ids)




print(df)
print(type(words))

collection = connectDb()

#wordDocument id dict
word_list_final = indexing_word_docs(words,ids,docs,collection)
#print(json.dumps(word_list_final[1]))



