import sys
import nltk
from pymongo import MongoClient
import codecs
import json
from nltk.corpus import stopwords

MONGO_HOST= 'mongodb://localhost/IBDtweetsDB'

stopwords = set(nltk.corpus.stopwords.words('english'))


client   = MongoClient(MONGO_HOST)
db       = client.IBDtweetsDB
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

for word, frequency in fdist.most_common(100):
	print(u'{};{}'.format(word, frequency)) 