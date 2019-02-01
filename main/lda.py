from pymongo import MongoClient
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim
from gensim import corpora

#Global variable
stopwords = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

#Database Setup
MONGO_HOST= 'mongodb://localhost/IBDtweetsDB'
client   = MongoClient(MONGO_HOST)
db       = client.IBDtweetsDB
count    = 0

#Cleaning and Preprocessing
def clean(doc):
    def replace_all(text, dic):
        global count
        for i, j in dic.iteritems():
            count = count + 1
            text = text.replace(i, j)
        return text
    # Replace synonyms into the same word
    replaceDic = {'Crohn': "ibd",'crohn\'s': "ibd",'ibd\'s':"ibd", 'ibds':"ibd", 'crohns': "ibd", 'cron\'s': "ibd", 'crons': "ibd", 'ulcerative': "ibd",'colitis': "ibd",
         'ibd': "ibd", 'inflammatory bowel': "ibd",'inflamatory bowel': "ibd", 'bowel disease': "ibd"}
    doc = replace_all(doc, replaceDic)

    doc = doc.replace('RT ', ' ')
    stop_free = " ".join([i for i in doc.lower().split() if i not in stopwords])
    punc_free = ''.join(char for char in stop_free if char not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

#Main Code
tweetsList    = []
for data in db.tweet.find({}, {"text":1, "_id":0}):
    tweetsList.append(data['text'])

# print(tweetsList[0])

cleanedTweetsList = [clean(tweet).split() for tweet in tweetsList]
print(count)

# print(cleanedTweetsList[0])

# Creating the term dictionary of our courpus, where every unique term is assigned an index. 
dictionary = corpora.Dictionary(cleanedTweetsList)
# print(dictionary)

# Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
doc_term_matrix = [dictionary.doc2bow(doc) for doc in cleanedTweetsList]

# Creating the object for LDA model using gensim library
Lda = gensim.models.ldamodel.LdaModel

# Running and Trainign LDA model on the document term matrix.
ldamodel = Lda(doc_term_matrix, num_topics=10, id2word = dictionary, passes=100)

# Print results
print(ldamodel.print_topics(num_topics=10, num_words=8))