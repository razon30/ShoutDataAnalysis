# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 20:01:48 2020

@author: Razon
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import nltk
from nltk.tokenize import WordPunctTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
import re


import cleaner as Cleaner

sb_stem = SnowballStemmer("english", ignore_stopwords=True)
pt_stem = PorterStemmer()
lmtzr = WordNetLemmatizer()
#textCleaner = Cleaner()

actualDataFile = r'D:\Software\Python\pyWorks\TweeterProject\code\ShoutTweet\WorksFromAnaconda\semiSupervised\LableledData16Aug20.xlsx'
cleanedDataFile = r'D:\Software\Python\pyWorks\TweeterProject\code\ShoutTweet\WorksFromAnaconda\semiSupervised\processedDataStepByStep.xlsx'
columnActualTweet = 'Tweet'
columnCleanedData = 'cleanedData'
columnWeightedValue = 'weight'
canNotConvert = 'cannot convert'
convert = 'convert'

cols = ['Tweet','Created At', 'labeling']

df = pd.read_excel(actualDataFile, header = None, names = cols)

def saveTheExcel():
    df.to_excel(cleanedDataFile, index = False)
    print("Saved the File")

def maskModel(existingText, newText):
    mask = df.label == existingText
    df.label[mask] = newText

# CLEANING DATA
tok = WordPunctTokenizer()
pattern1 = r'@[A-Za-z0-9]+'
pattern2 = r'https?://[A-Za-z0-9./]+'
combinedPattern = r'|'.join((pattern1, pattern2))

weight = []

def tweetCleaner(text):
    
# =============================================================================
#      #removing markup
#     if text == None or len(text) == 0:
#         text = convert
# =============================================================================
    
    text = text.lower()
    text = Cleaner.appos_look_up(text)
    text = Cleaner.remove_alphanumerics(text)
    text = Cleaner.remove_url(text)
  
    
    soup = BeautifulSoup(text, 'lxml')
    souped = soup.get_text()
    
    #removing '@' and HTTPs URL
    stripped = re.sub(combinedPattern, '', souped)
    
    #removing UTF-8 Bom text
    try:
        clean = stripped.decode("utf-8-sig").replace(u"\ufffd", "")
    except :
        clean = stripped
        
    #removing hashtag and numbers
    lettersOnly = re.sub("[^a-zA-Z]", " ", clean)
    
    #tokenization and removing extra white spaces
    words = tok.tokenize(lettersOnly)
    
    weightedValue = Cleaner.weightCalculator(words)
    weight.append(weightedValue)
    
    cleanedSentence = (" ".join(words)).strip()
    
    cleanedSentence = Cleaner.remove_single_char_word(cleanedSentence)
    cleanedSentence = Cleaner.remove_repeated_characters(cleanedSentence)
    cleanedSentence = Cleaner.remove_punctuations(cleanedSentence)
    cleanedSentence = Cleaner.remove_extra_space(cleanedSentence)
    #cleanedSentence = Cleaner.remove_stop_words(cleanedSentence)
    
    cleanedSentence = Cleaner.remove_key_words(cleanedSentence)
    
    cleanedSentence = Cleaner.removeStopWords(cleanedSentence)
    cleanedSentence = Cleaner.lemmatize_text(cleanedSentence)
    cleanedSentence = Cleaner.removeShortWords(cleanedSentence)
    
    
    return cleanedSentence


testing = df.Tweet[:]

testResult = []
for t in testing:
    t = str(t)
    #print("Before: "+str(t))
     #removing markup
    if t == None or len(str(t)) == 0:
        t = convert
    cleanded = tweetCleaner(t)
    #print("After: "+cleanded)
    testResult.append(cleanded)
    #print("=================================================\n")
    

df[columnCleanedData] = testResult
df[columnWeightedValue] = weight
saveTheExcel()
































# =============================================================================
# mask1 = df.label == 'Negative\n'
# df.label[mask1] = 'Negative'
# 
# mask2 = df.label == 'Neutral\n'
# df.label[mask2] = 'Neutral'
# 
# mask3 = df.label == 'Negative '
# df.label[mask3] = 'Negative'
# 
# mask4 = df.label == 'Neutral '
# df.label[mask4] = 'Neutral'
# 
# mask5 = df.label == 'Negative \n'
# df.label[mask5] = 'Negative'
# =============================================================================


