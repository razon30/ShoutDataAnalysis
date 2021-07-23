# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 19:36:56 2020

@author: Razon
"""
import pandas as pd

fileWithEmptyRow = r'D:\Software\Python\pyWorks\TweeterProject\code\ShoutTweet\WorksFromAnaconda\TrainData.xlsx'
fileWithOutRow = r'D:\Software\Python\pyWorks\TweeterProject\code\ShoutTweet\WorksFromAnaconda\TrainData1.xlsx'
columnNames = ['Tweet', 'Created At', 'labeling']

df = pd.read_excel(trainDataPath, header = None, names = cols)

def saveTheExcel():
    df.to_excel(fileWithOutRow, index = False)