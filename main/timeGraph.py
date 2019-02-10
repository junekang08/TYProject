# Libraries
from pymongo import MongoClient
from clean import clean
import re
from matplotlib import dates
from matplotlib import pyplot as plt
from datetime import time, timedelta

#Database Setup
MONGO_HOST= 'mongodb://junekang08:Rf860704!@cluster0-shard-00-00-cnddh.mongodb.net:27017,cluster0-shard-00-01-cnddh.mongodb.net:27017,cluster0-shard-00-02-cnddh.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin'
client   = MongoClient(MONGO_HOST)
db       = client.IBDTweets

#Main Code
tweetsList = []
times      = []
countDoc = 0
countDocWithTime = 0
for document in db.tweet.find({}, {"createdAt":1, "_id":0}):
    countDoc += 1
    if document.get('createdAt') is not None:
        countDocWithTime += 1
        createdAt = re.findall(r"[0-9][0-9](?=:)",document.get('createdAt'))
    hour = createdAt[0]
    minute = createdAt[1]
    timeObject = time(int(hour), int(minute))
    times.append(timeObject)
print countDoc, countDocWithTime
# initialize one empty bucket per day
buckets = [0 for i in range(24)]

for t in times:
    buckets[t.hour] += 1

# print a bar plot of the results
plt.bar(range(24), buckets)
# add x-axis ticks (dates)
plt.xticks(range(24), range(24), rotation=70)

# some cosmetics: hide all ticks
plt.setp(plt.gca().get_xticklabels(), visible=False)
# show every 4th tick again
plt.setp(plt.gca().get_xticklabels()[::4],visible=True)

# show the result
plt.show()