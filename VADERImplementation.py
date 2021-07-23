# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 01:25:20 2021

@author: razon
"""

import re, numpy as np, pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

cleanedDataFile = r'D:\Software\Python\pyWorks\TweeterProject\code\ShoutTweet\WorksFromAnaconda\semiSupervised\DSCwoKey-22-8-20.xlsx'
columnActualTweet = 'Tweet'
columnCleanedData = 'cleanedData'
convert = 'convert'
labeling = 'labeling'

df = pd.read_excel(cleanedDataFile)
data = df[columnCleanedData].tolist()

#print(data)

sentiment_dict = []

def sentiment_scores(sent):
# Create a SentimentIntensityAnalyzer object.
    sentence = str(sent)
    sid_obj = SentimentIntensityAnalyzer()
# polarity_scores method of SentimentIntensityAnalyzer
# oject gives a sentiment dictionary.
# which contains pos, neg, neu, and compound scores.
    sentScore = sid_obj.polarity_scores(sentence)
    #print(sentScore)
    return sentScore['compound']


for i in range(len(data)):
    sentiment_dict.append(sentiment_scores(data[i]))


#print(sentiment_dict)
#dictData = [[x,sentiment_dict.count(x)] for x in set(sentiment_dict)]

aDic = dict((x,sentiment_dict.count(x)) for x in set(sentiment_dict))

keys = aDic.keys()
values = aDic.values()

plt.bar(keys, values)
plt.show()

#print(dictData)














