# -*- coding: utf-8 -*-
"""
Created on Wed May  6 21:00:00 2020

@author: Razon
"""

from nltk.corpus import wordnet


def synonymAntonym(word, sent):
    
    synonyms = set()
    antonyms = set()
    
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.add(l.name())
            if l.antonyms():
                antonyms.add(l.antonyms()[0].name())
                
    #print(synonyms)
    #print(antonyms)
    
    point = 0
    
    point = countSynonym(sent, synonyms) #- countAntonym(sent, antonyms)
    
    return point

def countSynonym(sent, synonyms):
    point = 0
    
    for syn in synonyms:
        if syn in sent:
            point = point + 1
    
    #print("Syn point: "+ str(point))
    return point

def countAntonym(sent, antonyms):
    point = 0
    
    for ant in antonyms:
        if ant in sent:
            point = point + 1
    
    #print("Ant point: "+ str(point))
    return point



word = "angry"
sent = ['I', 'am', 'glad', 'it', 'was', 'felicitous', 'angry', 'unhappy', 'unangry', '.']
point = synonymAntonym(word, sent)
print("total point: "+ str(point))






