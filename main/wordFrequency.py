import sys
import nltk
from pymongo import MongoClient
import codecs
import json
from nltk.corpus import stopwords

MONGO_HOST= 'mongodb://junekang08:Rf860704!@cluster0-shard-00-00-cnddh.mongodb.net:27017,cluster0-shard-00-01-cnddh.mongodb.net:27017,cluster0-shard-00-02-cnddh.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin'

stopwords = set(nltk.corpus.stopwords.words('english'))

client   = MongoClient(MONGO_HOST)
db       = client.IBDTweets
texts    = []
for data in db.tweet.find({}, {"text":1, "_id":0}):
	texts.append(data['text'])
tweetText = ''.join(texts)
# print(tweetText)

words = nltk.word_tokenize(tweetText)

words = [word for word in words if len(word) > 1]

words = [word.lower() for word in words]

words = [word for word in words if word not in stopwords]

fdist = nltk.FreqDist(words)

for word, frequency in fdist.most_common(10):
	print(u'{};{}'.format(word, frequency)) 