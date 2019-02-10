# Libraries
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from clean import clean
from pymongo import MongoClient

#Database Setup
MONGO_HOST= 'mongodb://junekang08:Rf860704!@cluster0-shard-00-00-cnddh.mongodb.net:27017,cluster0-shard-00-01-cnddh.mongodb.net:27017,cluster0-shard-00-02-cnddh.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin'
client   = MongoClient(MONGO_HOST)
db       = client.IBDTweets

#Main Code
tweetsList = []
for document in db.tweet.find({}, {"text":1, "_id":0}):
    tweetsList.append(document.get("text"))
cleanedTweetsList = [clean(''.join(tweet)) for tweet in tweetsList]
text = (" ".join(cleanedTweetsList))

# Create the wordcloud object
wordcloud = WordCloud(width=480, height=480, collocations = False, margin=0).generate(text)
 
# Display the generated image:
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()