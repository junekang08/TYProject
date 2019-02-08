# -*- coding: utf-8 -*-
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import re

#Global variable
stopwords = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

#Cleaning and Preprocessing
def clean(doc):
    def replace_all(text, dic):
        for i, j in dic.iteritems():
            text = text.replace(unicode(i,"utf-8"), j)
        return text
    # Replace synonyms into the same word
    replaceDic = {'Crohn': "ibd","crohn’s": "ibd","ibd’s":"ibd", "ibd's":"ibd", "ibds":"ibd", 'crohns': "ibd", "cron’s": "ibd", 
                    'crons': "ibd", 'ulcerative': "ibd",'colitis': "ibd",'ibd': "ibd", 'inflammatory bowel disease': "ibd",
                    'inflamatory bowel disease': "ibd", 'bowel disease': "ibd",'inflammatory bowel': "ibd",'inflamatory bowel': "ibd", 
                    "amp": "", "’": "'", "IBD’s": "ibd", "IBD's": "ibd", "IBDs": "ibd", "IBDS": "ibd", "IBD'S": "ibd", "rt ": ""}
    doc = doc.replace(",", " ")
    stop_free = " ".join([i for i in doc.lower().split() if i not in stopwords])
    punc_free = ''.join(char for char in stop_free if char not in exclude)
    punc_free = replace_all(punc_free, replaceDic)
    punc_free = re.sub(r"http\S+", "", punc_free)

    normalized = " ".join(lemma.lemmatize(word, pos="v") for word in punc_free.split())
    return normalized.encode("utf8")