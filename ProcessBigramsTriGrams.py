# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 22:07:19 2020

@author: Razon
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import re
import nltk
import seaborn as sns
import warnings

from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords
from nltk import pos_tag, sent_tokenize, word_tokenize, BigramAssocMeasures,\
    BigramCollocationFinder, TrigramAssocMeasures, TrigramCollocationFinder
from subprocess import check_output
from nltk import WordNetLemmatizer
import string


cleanedDataFile = r'D:\Software\Python\pyWorks\TweeterProject\code\ShoutTweet\WorksFromAnaconda\semiSupervised\DSCwoKey-22-8-20.xlsx'  
columnActualTweet = 'Tweet'
columnCleanedData = 'cleanedData'
convert = 'convert'
labeling = 'labeling'


tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()
testData = pd.read_excel(cleanedDataFile)


texts = []

# loop through document list
for i in testData[columnCleanedData]:
    
    # clean and tokenize document string
    i = str(i)
    raw = i.lower()
    tokens = tokenizer.tokenize(raw)

    # remove stop words from tokens
    stopped_tokens = [j for j in tokens if not j in en_stop]
    
    # strip tokens
    stemmed_tokens = [j.strip() for j in stopped_tokens]
    
    stemmed_tokens = [j for j in stemmed_tokens if j not in set(['nan', 'u'])]
    
    # add tokens to list
    texts.append(stemmed_tokens)


def get_bitrigrams(full_text, threshold=30):
    full_text = str(full_text)
    if isinstance(full_text, str):
        text = full_text
    else:
        text = " ".join(full_text)
    bigram_measures = BigramAssocMeasures()
    trigram_measures = TrigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(text.split())
    finder.apply_freq_filter(3)
    bigrams = {" ".join(words): "_".join(words)
               for words in finder.above_score(bigram_measures.likelihood_ratio, threshold)}
#     finder = TrigramCollocationFinder.from_words(text.split())
#     finder.apply_freq_filter(3)
#     trigrams = {" ".join(words): "_".join(words)
#                 for words in finder.above_score(trigram_measures.likelihood_ratio, threshold)}
    return bigrams #, trigrams


def process_text(text, lemmatizer, translate_table, stopwords):
    processed_text = ""
    text = str(text)
    for sentence in sent_tokenize(text):
        tagged_sentence = pos_tag(word_tokenize(sentence.translate(translate_table)))
        for word, tag in tagged_sentence:
            word = word.lower()
            if word not in stopwords:
                if tag[0] != 'V':
                    processed_text += lemmatizer.lemmatize(word) + " "
    return processed_text


wordnet_lemmatizer = WordNetLemmatizer()
stop = set(stopwords.words('english'))
translate_table = dict((ord(char), " ") for char in string.punctuation)


def use_ngrams_only(texts, lemmatizer, translate_table, stopwords):
    processed_texts = []
    for index, doc in enumerate(texts):
        processed_texts.append(process_text(doc, wordnet_lemmatizer, translate_table, stop))
    bigrams = get_bitrigrams(processed_texts)
    indexed_texts = []
    for doc in processed_texts:
        current_doc = []
#         for k, v in trigrams.items():
#             c = doc.count(k)
#             if c > 0:
#                 current_doc += [v] * c
#                 doc = doc.replace(k, v)
        for k, v in bigrams.items():
            current_doc += [v] * doc.count(" " + k + " ")
        indexed_texts.append(" ".join(current_doc))
    return " ".join(indexed_texts)




def drawTheImage(texts):
    wordcloud = WordCloud(width = 800, 
                          height = 500, 
                          random_state=21, 
                          max_font_size=110,  
                          collocations=False).generate(use_ngrams_only(texts, 
                                                                       wordnet_lemmatizer, 
                                                                       translate_table, 
                                                                       stop)
                                                                       )
    plt.figure(figsize=(10,7))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    plt.show()
    
    
drawTheImage(texts)
    
#print(texts)

























