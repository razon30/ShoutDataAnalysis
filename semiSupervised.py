# -*- coding: utf-8 -*-
"""
Created on Mon May 11 19:08:24 2020

@author: Razon
"""

import pandas as pd
from nltk.tokenize import WordPunctTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
import re
import cleaner as Cleaner
import SynNonymAntonym as syn

sb_stem = SnowballStemmer("english", ignore_stopwords=True)
pt_stem = PorterStemmer()
lmtzr = WordNetLemmatizer()
#textCleaner = Cleaner()


trainDataPath = r'D:\Software\Python\pyWorks\TweeterProject\code\ShoutTweet\WorksFromAnaconda\semiSupervised\labeledDataTest.xlsx'
notlabeled = r'D:\Software\Python\pyWorks\TweeterProject\code\ShoutTweet\WorksFromAnaconda\semiSupervised\notlabeled.xlsx'
columnActualTweet = 'tweet'
columnCleanedData = 'cleanedData'
columnCleanedDataNew = 'newCleanedData'
columnWeightedValue = 'weight'
label = 'label'

cols = ['id', 'tweet', 'label', 'newCleanedData', 'weight', 'cleanedData', 'label1', 'POS']

df = pd.read_excel(trainDataPath, header = None, names = cols)
df1 = pd.read_excel(notlabeled, header = None, names = cols)

def saveTheExcel():
    df.to_excel(trainDataPath, index = False)

def maskModel(existingText, newText):
    mask = df.label == existingText
    df.label[mask] = newText

 # CLEANING DATA
tok = WordPunctTokenizer()
pattern1 = r'@[A-Za-z0-9]+'
pattern2 = r'https?://[A-Za-z0-9./]+'
combinedPattern = r'|'.join((pattern1, pattern2))

weight = []

labeledPOS = []
unlabeledPOS = []
newLabels = []


def POS(labelText, unlabeledText):
    
    labelTextArray = tok.tokenize(labelText)
    unlabeledTextArray = tok.tokenize(unlabeledText)
    
    labelPosWords = Cleaner.getPOS(labelTextArray)
    unLabelPosWords = Cleaner.getPOS(unlabeledTextArray)
    
    labeledPOS.append(labelPosWords)
    unlabeledPOS.append(unLabelPosWords)
    
    

def defineLabel(labelArray, unlabelArrray):
    point = 0
    for word in unlabelArrray:
        point = point + syn.synonymAntonym(word, labelArray)
        
    return point
        

    

unlabeledTesting = df1.newCleanedData[:]
labeledTesting = df.newCleanedData[:len(unlabeledTesting)]
labels = df.label[:len(unlabeledTesting)]
    
for i in range(0, len(unlabeledTesting)):
    unlabeledClean = unlabeledTesting[i]
    labeledClean = labeledTesting[i]
   # print(i)
   # print(unlabeledClean)
   # print("\n")
   # print(labeledClean)
   # print("\n\n")
    POS(labeledClean, unlabeledClean)
    
    

    

for i in range(0, len(unlabeledPOS)):
     unlabelPOSItem = unlabeledPOS[i]
     maxPoint = 0
     lab = labels[i]
     for j in range(0, len(labeledPOS)):
         labelPOSItem = labeledPOS[j]
         point = defineLabel(labelPOSItem, unlabelPOSItem)
         if point > maxPoint:
# =============================================================================
#              print(lab)
#              print(maxPoint)
#              print("\n")
# =============================================================================
             maxPoint = point
             lab = labels[j]
# =============================================================================
#              print(str(i) + "   "+ str(j))
#              print(lab)
#              print(maxPoint)
#              print("\n\n\n")
# =============================================================================
     newLabels.append(lab)
     

df1[label] = newLabels
df1.to_excel(notlabeled, index = False)
    
     
# =============================================================================
#      print(i)
#      print(unlabelPOSItem)
#      print("\n")
#      print(labelPOSItem)
#      print("\n\n")
# =============================================================================
























































