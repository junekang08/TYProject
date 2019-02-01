import sys
import nltk
import codecs
from nltk.corpus import stopwords

stopwords = set(nltk.corpus.stopwords.words('english'))

document = "hello world hello world hello"

words = nltk.word_tokenize(document)

words = [word for word in words if len(word) > 1]

words = [word.lower() for word in words]

words = [word for word in words if word not in stopwords]

fdist = nltk.FreqDist(words)

for word, frequency in fdist.most_common(50):
print(u'{};{}'.format(word, frequency)) 