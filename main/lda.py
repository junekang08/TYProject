from pymongo import MongoClient
from nltk.util import ngrams
import gensim
from gensim import corpora
from clean import clean

#Database Setup
MONGO_HOST= 'mongodb://junekang08:Rf860704!@cluster0-shard-00-00-cnddh.mongodb.net:27017,cluster0-shard-00-01-cnddh.mongodb.net:27017,cluster0-shard-00-02-cnddh.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin'
client   = MongoClient(MONGO_HOST)
db       = client.IBDTweets

#Main Code
tweetsList    = []
for data in db.tweet.find({}, {"text":1, "_id":0}):
    tweetsList.append(data['text'])

cleanedTweetsList = [clean(''.join(tweet)).split() for tweet in tweetsList]
print 'size: ', len(cleanedTweetsList)
# for tweet in range(len(cleanedTweetsList)):
#     cleanedTweetsList[tweet] = cleanedTweetsList[tweet] + ["_".join(w) for w in ngrams(cleanedTweetsList[tweet], 2)]
# print(cleanedTweetsList[0])

# Creating the term dictionary of our courpus, where every unique tercm is assigned an index. 
dictionary = corpora.Dictionary(cleanedTweetsList)

# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
doc_term_matrix = [dictionary.doc2bow(doc) for doc in cleanedTweetsList]

# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

# Running and Trainign LDA model on the document term matrix.
ldamodel = Lda(doc_term_matrix, num_topics=20, id2word = dictionary, passes=100)

# Print results
for topic in ldamodel.print_topics(num_topics=20, num_words=8):
    print (topic, "\n")