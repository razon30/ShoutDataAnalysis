# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 23:38:59 2020

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

appose = []
columnapostrophes = 'apostrophes'

aplhaneu = []
columnalphanumeric = 'alphanumeric'

url = []
columnURL = 'URL'

htmlXml = []
columnhtmlXml = 'htmlXml'

tokenize = []
columntokenize = 'Tokenize'

hashtagMention = []
columnhashtagMention = 'hashtagMention'

singleLetter = []
columnsingleLetter = 'SingleLetter'

repeateCharacter = []
columnrepeateCharacter = 'repeateCharacter'

puctuation = []
columnpuctuation = 'puctuation'

keywords = []
columnKeywords = 'Keywords'

stopWords = []
columnStropWords = 'StropWords'

lemmatize = []
columnlemmatize = 'lemmatize'

shortWord = []
columnShortWords = 'ShortWords'



def tweetCleaner(text):
    
# =============================================================================
#      #removing markup
#     if text == None or len(text) == 0:
#         text = convert
# =============================================================================
    
    text = text.lower()
    text = Cleaner.appos_look_up(text)
    appose.append(text)
    
    text = Cleaner.remove_alphanumerics(text)
    aplhaneu.append(text)
    
    text = Cleaner.remove_url(text)
    url.append(text)
  
    
    soup = BeautifulSoup(text, 'lxml')
    souped = soup.get_text()
    
    #removing '@' and HTTPs URL
    stripped = re.sub(combinedPattern, '', souped)
    
    #removing UTF-8 Bom text
    try:
        clean = stripped.decode("utf-8-sig").replace(u"\ufffd", "")
    except :
        clean = stripped
        
    htmlXml.append(clean)
    
    #removing hashtag and numbers
    lettersOnly = re.sub("[^a-zA-Z]", " ", clean)
    hashtagMention.append(lettersOnly)
    
    #tokenization and removing extra white spaces
    words = tok.tokenize(lettersOnly)
    tokenize.append(words)
    
    weightedValue = Cleaner.weightCalculator(words)
    weight.append(weightedValue)
    
    cleanedSentence = (" ".join(words)).strip()
    
    cleanedSentence = Cleaner.remove_single_char_word(cleanedSentence)
    singleLetter.append(cleanedSentence)
    
    cleanedSentence = Cleaner.remove_repeated_characters(cleanedSentence)
    repeateCharacter.append(cleanedSentence)
    
    cleanedSentence = Cleaner.remove_punctuations(cleanedSentence)
    puctuation.append(cleanedSentence)
    
    cleanedSentence = Cleaner.remove_extra_space(cleanedSentence)
    #appose.append(clean)
    
    #cleanedSentence = Cleaner.remove_stop_words(cleanedSentence)
    
    cleanedSentence = Cleaner.remove_key_words(cleanedSentence)
    keywords.append(cleanedSentence)
    
    cleanedSentence = Cleaner.removeStopWords(cleanedSentence)
    stopWords.append(cleanedSentence)
    
    cleanedSentence = Cleaner.lemmatize_text(cleanedSentence)
    lemmatize.append(cleanedSentence)
    
    cleanedSentence = Cleaner.removeShortWords(cleanedSentence)
    shortWord.append(cleanedSentence)
    
    
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

df[columnapostrophes] = appose 
df[columnalphanumeric] = aplhaneu 
df[columnURL] = url 
df[columnhtmlXml] = htmlXml 
df[columntokenize] = tokenize 
df[columnhashtagMention] = hashtagMention 
df[columnsingleLetter] = singleLetter 
df[columnrepeateCharacter] = repeateCharacter 
df[columnpuctuation] = puctuation 
df[columnKeywords] = keywords 
df[columnStropWords] = stopWords 
df[columnlemmatize] = lemmatize 
df[columnShortWords] = shortWord 


#df[columnWeightedValue] = weight
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


