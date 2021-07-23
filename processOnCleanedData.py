# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 21:49:54 2020

@author: Razon
"""
import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import re
import nltk
import seaborn as sns
import warnings


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


#==========================START PIE CHART ===============================

def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%".format(pct, absolute)

def drawPieChart(dataArray, typeHeader, mainHeader):
    fig, ax = plt.subplots(figsize=(10, 5), subplot_kw=dict(aspect="equal"))
    data = [float(x.split()[0]) for x in dataArray]
    ingredients = [x.split()[-1] for x in dataArray]
    wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                  textprops=dict(color="w"))
    ax.legend(wedges, ingredients,
          title=typeHeader,
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=8, weight="bold")
    ax.set_title(mainHeader)
    plt.show()


#==========================END PIE CHART============================

#=====================START NUMBER OF TWEET CATEGORY==============================

posTweet = 0
negTweet = 0
neuTweet = 0

# =============================================================================
# for i in range(len(testData[labeling])):
#     label = testData[labeling][i]
#     label = str(label)
#     if label == '0.0':
#         posTweet += 1
#     elif label == '1.0':
#         negTweet += 1
#     elif label == '2.0':
#         neuTweet +=1 
# 
# data = ["{} g Positive".format(posTweet),
#           "{} g Negative".format(negTweet),
#           "{} g Neutral".format(neuTweet)]
# 
# drawPieChart(data, "", "Proportion of emotions in tweets")
# =============================================================================

#===============================Word Cloud==================================
#all_words = ' '.join([str(text) for text in testData[columnCleanedData]])

# =============================================================================
positiveWords = ' '.join([str(text) for text in testData[columnCleanedData]])
print(positiveWords)
# negativeWords = ' '.join([str(text) for text in testData[columnCleanedData][testData[labeling] == 1]])
# neutralWords = ' '.join([str(text) for text in testData[columnCleanedData][testData[labeling] == 2]])
# =============================================================================

def drawTheImage(data):
    wordcloud = WordCloud(width = 800, height = 500, random_state=21, max_font_size=110,  collocations=False).generate(data)
    plt.figure(figsize=(10,7))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    plt.show()
    
#drawTheImage(all_words)
# =============================================================================
# drawTheImage(negativeWords)
# drawTheImage(neutralWords)
# =============================================================================
#===============================Word Cloud==================================

#===============================LDA Algorithm==================================

    # list for tokenized documents in loop
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

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)
    
# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=10, id2word = dictionary, passes=2)

for idx, topic in ldamodel.print_topics(-1):
    print('Topic: {} \nWords: {}'.format(idx, topic))
    
    
from pyLDAvis import sklearn as sklearn_lda
import pickle 
import pyLDAvis




#===============================LDA Algorithm==================================
    
#===============================Bar chart==================================
     
def countWords(x):
    hashtags = []
    for i in x:
        i = str(i).lower()
        ht = re.findall(r"(\w+)", i)
        if 'http' in ht:
            ht.remove('http')
        if 'https' in ht:
            ht.remove('https')
        hashtags.append(ht)
    return hashtags

def getWordsMapCount(n):
     HT_normal = countWords(testData[columnCleanedData])
     return sum(HT_normal, [])
# =============================================================================
#      if n == 0:
#         HT_normal = countWords(testData[columnCleanedData][testData[labeling] == 0])
#         return sum(HT_normal, [])
#      elif n == 1:
#         HT_negative = countWords(testData[columnCleanedData][testData[labeling] == 1])
#         return  sum(HT_negative, [])
#      elif n == 2:
#         HT_negative = countWords(testData[columnCleanedData][testData[labeling] == 2])
#         return  sum(HT_negative, [])
# 
# =============================================================================

def printBarChart(data):
    a = nltk.FreqDist(data)
    d = pd.DataFrame(
         {'Word' : list(a.keys()),
         'Count': list(a.values())
         })

    #selecting top 10 most frequesnt words
    d = d.nlargest(columns="Count", n = 15)
    plt.figure(figsize=(20,10))
    ax = sns.barplot(data=d, x="Word", y="Count")
    ax.set(ylabel = 'Count')
    plt.show()

#Printing top 'n' hashtags
#printBarChart(getWordsMapCount(0))
# =============================================================================
# printBarChart(getWordsMapCount(1))
# printBarChart(getWordsMapCount(2))
# =============================================================================
    
    
    
# =============================================================================
#     
# Topic: 0 
# Words: 0.018*"life" + 0.015*"anxiety" + 0.012*"issue" + 0.012*"people" + 0.010*"depression" + 0.010*"family" + 0.010*"health" + 0.008*"year" + 0.008*"many" + 0.008*"problem"
# Topic: 1 
# Words: 0.018*"much" + 0.015*"get" + 0.013*"need" + 0.013*"time" + 0.011*"day" + 0.011*"take" + 0.008*"people" + 0.008*"sick" + 0.008*"know" + 0.008*"today"
# Topic: 2 
# Words: 0.021*"day" + 0.015*"like" + 0.014*"get" + 0.013*"week" + 0.011*"time" + 0.010*"feel" + 0.010*"go" + 0.010*"got" + 0.009*"thing" + 0.009*"back"
# Topic: 3 
# Words: 0.023*"reduce" + 0.021*"via" + 0.020*"success" + 0.019*"burnout" + 0.017*"help" + 0.017*"uk" + 0.010*"learn" + 0.009*"cope" + 0.009*"tip" + 0.009*"business"
# Topic: 4 
# Words: 0.038*"mindfulness" + 0.035*"stressed" + 0.023*"employee" + 0.022*"hour" + 0.019*"study" + 0.016*"week" + 0.015*"according" + 0.015*"peace" + 0.014*"survey" + 0.012*"recent"
# Topic: 5 
# Words: 0.018*"way" + 0.016*"teacher" + 0.014*"time" + 0.011*"cbd" + 0.010*"school" + 0.009*"new" + 0.008*"best" + 0.007*"day" + 0.007*"home" + 0.007*"help"
# Topic: 6 
# Words: 0.022*"workplace" + 0.014*"wellbeing" + 0.013*"tip" + 0.012*"managing" + 0.011*"deal" + 0.011*"employee" + 0.010*"cloud" + 0.010*"article" + 0.010*"read" + 0.009*"health"
# Topic: 7 
# Words: 0.046*"health" + 0.023*"business" + 0.018*"mental" + 0.018*"productivity" + 0.018*"exercise" + 0.017*"beat" + 0.016*"fitness" + 0.014*"increase" + 0.014*"diet" + 0.012*"help"
# Topic: 8 
# Words: 0.102*"like" + 0.098*"fun" + 0.087*"play" + 0.080*"begin" + 0.055*"sa" + 0.023*"na" + 0.019*"inspiration" + 0.017*"pa" + 0.013*"ko" + 0.010*"ako"
# Topic: 9 
# Words: 0.038*"age" + 0.013*"long" + 0.011*"quote" + 0.010*"working" + 0.009*"burnout" + 0.008*"worker" + 0.008*"home" + 0.008*"hour" + 0.006*"food" + 0.006*"life"
# =============================================================================

























