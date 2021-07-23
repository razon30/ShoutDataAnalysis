# -*- coding: utf-8 -*-
"""
Created on Mon May 11 21:26:20 2020

@author: Razon
"""

import pandas as pd


compare = r'D:\Software\Python\pyWorks\TweeterProject\code\ShoutTweet\WorksFromAnaconda\semiSupervised\compare.xlsx'
cols1 = ['id', 'tweet', 'label']

notlabeled = r'D:\Software\Python\pyWorks\TweeterProject\code\ShoutTweet\WorksFromAnaconda\semiSupervised\notlabeled.xlsx'
cols2 = ['id', 'tweet', 'label', 'newCleanedData', 'weight', 'cleanedData', 'label1', 'POS']

label = 'label'

df = pd.read_excel(compare, header = None, names = cols1)
df1 = pd.read_excel(notlabeled, header = None, names = cols2)

labels = df.label[:]
newLabels = df1.label[:]

match = 0

for i in range(0, len(newLabels)):
    
    if labels[i] == newLabels[i]:
        match = match + 1
        
        
print(match , " Out of ", len(newLabels))