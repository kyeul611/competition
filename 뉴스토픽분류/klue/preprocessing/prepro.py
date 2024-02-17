import numpy as np
import pandas as pd
import os
import re
import hanja
import tqdm
from hanspell import spell_checker

def mergeData(path1, path2, isTopic=True):
    
    df1 = pd.read_csv(path1)
    df2 = pd.read_csv(path2)
    
    if isTopic == True:
        new_data = pd.merge(df1, df2[['title','topic_idx']], how='outer')
    else:
        new_data = pd.merge(df1, df2[['title']], how='outer')
        
    return new_data

def replaceChar(data, isTopic=True):
    
    switchar= []
    
    chars = open("./preprocessing/replace_words.txt", encoding='utf-8')
    
    for char in chars:
        switchar.append(char.strip().split("\t"))
        
    if isTopic == True:
        switched_data = pd.DataFrame(columns=["index", "title", "topic_idx"])
    else:
        switched_data = pd.DataFrame(columns=["index", "title"])
        
    for i in tqdm.tqdm(range(len(data))):
        title = data.iloc[i]['title']
        for j in switchar:
            title = re.sub(j[0], j[1]+' ', title)
        title = hanja.translate(' '.join(hanja.split_hanja(title)), 'substitution')
        title = re.sub("[^가-힣0-9a-zA-Z%]",' ', title)
        
        if isTopic == True:
            switched_data = switched_data.append(pd.DataFrame(data=[[i, title, data.iloc[i]["topic_idx"]]], columns=['index', 'title', 'topic_idx']))
        else:
            switched_data = switched_data.append(pd.DataFrame(data=[[i, title]], columns=['index', 'title']))
    
    return switched_data

def spellcheck(sents):
    
    spaced_data = []
    
    for sent in tqdm.tqdm(sents):
        
        spelled_sent = spell_checker.check(sent)
        spaced_data.append(spelled_sent.checked)
        
    return spaced_data