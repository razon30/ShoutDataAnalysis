# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 20:00:37 2020

@author: Razon
"""

"""
Necessary URLs:
    https://towardsdatascience.com/extracting-twitter-data-pre-processing-and-sentiment-analysis-using-python-3-0-7192bd8b47cf
    https://github.com/reZach/grammarify
    https://github.com/s/preprocessor
    https://github.com/abdulfatir/twitter-sentiment-analysis/blob/master/code/preprocess.py
    https://www.programiz.com/python-programming
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

# =============================================================================
# from appos.appos import appos_dict as apposDict
# from slangs.slangs import slangs_dict as slangDict
# from stopwords.stopwords import stop_words_list as stopWordList
# from emoticons.emo import emo as emoList
# =============================================================================
import cleaner as Cleaner

sb_stem = SnowballStemmer("english", ignore_stopwords=True)
pt_stem = PorterStemmer()
lmtzr = WordNetLemmatizer()
#textCleaner = Cleaner()

trainDataPath = r'D:\Software\Python\pyWorks\TweeterProject\code\ShoutTweet\WorksFromAnaconda\TrainData.xlsx'
trainDataPath1 = r'D:\Software\Python\pyWorks\TweeterProject\code\ShoutTweet\WorksFromAnaconda\TrainData1.xlsx'
columnActualTweet = 'tweet'
columnCleanedData = 'cleanedData'
columnCleanedDataNew = 'newCleanedData'
columnWeightedValue = 'weight'

cols = ['id', 'tweet', 'label', 'label1', 'cleanedData', 'newCleanedData', 'weight']
#cols = ['id', 'tweet', 'label', 'newCleanedData', 'weight', 'cleanedData', 'label1']

df = pd.read_excel(trainDataPath, header = None, names = cols)

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

def tweetCleaner(text):
    
    text = Cleaner.appos_look_up(text)
    text = Cleaner.remove_alphanumerics(text)
    text = Cleaner.remove_url(text)
  
    
    #removing markup
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
    cleanedSentence = Cleaner.remove_stop_words(cleanedSentence)
    
    
    return cleanedSentence

testing = df.tweet[:]

testResult = []
for t in testing:
   # print("Before: "+t)
    cleanded = tweetCleaner(t)
    #print("After: "+cleanded)
    testResult.append(cleanded)
    #print("=================================================\n")
    

df[columnCleanedDataNew] = testResult
df[columnWeightedValue] = weight
saveTheExcel()




# =============================================================================
# 
# 
# cleanedSentence = Cleaner.lemmatize_text("been had done languages cities mice")
# print(cleanedSentence)
# 
# 
# 
# 
# 
# 
# 
# 
# from nltk.tokenize import word_tokenize
# 
# lemmatizer = WordNetLemmatizer()
# 
# print(lemmatizer.lemmatize("studying", pos='n'))
# # pos: parts of speech tag, verb
# print(lemmatizer.lemmatize("studying", pos='v'))
# 
# lemmatizer=WordNetLemmatizer()
# input_str= "He has been studying very hard" #"been had done languages cities mice"
# input_str=word_tokenize(input_str)
# pos = Cleaner.getPOS(input_str)
# print(pos)
# for word in input_str:
#     print(lemmatizer.lemmatize(word))
# =============================================================================


































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


