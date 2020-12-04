# Twitter-Search-Engine
Search Engine for Tweets - Project for Course Big Data Algorithms CMPE297


Main features of web application:  
- Search on Tweet text
- Filter on fields such as username, user location, users mentioned and hashtags 

Tools Used: 

- Tweepy, Pymongo, Flask, Reactjs, Tweet-Preprocessor, Sklearn, Pandas

Architectural Overview:  

<img src="https://github.com/purvimisal/Twitter-Search-Engine/blob/main/ss/archoverview.jpg" width="500">


Screenshots of application: 

<img src="https://github.com/purvimisal/Twitter-Search-Engine/blob/main/ss/searchtext.png" width="700">
<img src="https://github.com/purvimisal/Twitter-Search-Engine/blob/main/ss/searchfields.png" width="700">


## Installation Guide:

### For Linux Systems

Install requirements:   
Go to the api folder 
#### `pip3 install -r requirements.txt`


Steps to Collect and Index data:  

1. Enter Twitter Developer API credentials in the given strings in scripts/stream.py script
2. Run stream.py to create an intermediate JSON file in the same directory
3. Enter MongoDB connection string in the given string in scripts/store.py 
4. Run store.py to relay all the tweets from JSON file to MongoDB twitter_collection.
5. Run search.py to create TF-IDF indexing of tweets from twitter_collection and store the tf-idf scores in the respective collection in MongoDB.  
**(Data collected is of topic Sports)



Start the Flask backend application
```
flask run
```

### For Windows
* Install _Pipenv_

```
pip install pipenv
```

* Install _[Flask](https://palletsprojects.com/p/flask/)_

```
pipenv install flask==1.1.1
```
Set flask_app
```
set FLASK_APP=app.py
```

then ```dir``` to check the current directory

```
pipenv shell
```

Install requirements
### `pip3 install -r requirements.txt`

inside the shell

```
flask run
```

### Frontend 


#### Available Scripts

In the twitter-frontend directory, you can run:
```
npm install
```
Start the React App 
```
npm start
```
