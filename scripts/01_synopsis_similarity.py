# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 02:07:11 2020

@author: Jothimani
"""

import pandas as pd
import os 
import nltk
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy

nlp = spacy.load('en_core_web_lg')

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')


from nltk.corpus import stopwords
import re
import string
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
from nltk.corpus import stopwords
stop = stopwords.words('english')
stop_words_ = set(stopwords.words('english'))
wn = WordNetLemmatizer()

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)


os.chdir("C:/Users/Jothimani/Documents/GR")

books_db = pd.read_csv(r"book_data_bk.csv",encoding = "ISO-8859-1", engine='python')
print(books_db.head())
print(books_db.shape)
book_db1 = books_db.drop_duplicates(keep = 'first', inplace = False)
print(book_db1.shape)
book_db = book_db1.dropna()
print(book_db.shape)
book_db.to_csv("book_data_bk.csv",encoding = "ISO-8859-1")

print(book_db.columns)

book_subset = book_db[['book_title','book_authors','book_desc']]
print(book_subset.shape)

book_subset.isnull().values.any()

book_subset_NA = book_subset.dropna()
book_subset_NA.isnull().values.any()
book_subset_NA = book_subset_NA.reset_index()

def black_txt(token):
    return  token not in stop_words_ and token not in list(string.punctuation)  and len(token)>2   
  
def clean_txt(text):
  clean_text = []
  clean_text2 = []
  text = re.sub("'", "",text)
  text=re.sub("(\\d|\\W)+"," ",text) 
  text = text.replace("nbsp", "")
  clean_text = [ wn.lemmatize(word, pos="v") for word in word_tokenize(text.lower()) if black_txt(word)]
  clean_text2 = [word for word in clean_text if black_txt(word)]
  return " ".join(clean_text2)


book_subset_NA['book_desc'] = book_subset_NA['book_desc'].apply(clean_txt)


#Recommendation Using Spacy 
#Transform the corpus of text to the Spacy's documents 
import time 

def transformSpacy(df, index):
    time.perf_counter()
    list_docs = []
    for i in range(len(df)):
        try:
            if i != index:
                doc = nlp("u'" + df['book_desc'][i] + "'")
                #doc = nlp(' '.join([str(t) for t in df['book_desc'][i] if not t.is_stop]))
                list_docs.append((doc,i))
            else:
                continue
        except:
            continue
    print(len(list_docs))
    return(list_docs)




def calculateSimWithSpaCy(nlp, j, df, list_docs, user_text, book_title, n=6):
    # Calculate similarity using spaCy
    list_sim =[]
    doc1 = nlp("u'" + user_text + "'")
    for i in df.index:
      try:
          if i != j:
              doc2 = list_docs[i][0]
              score = doc1.similarity(doc2)
              print("user given:", book_title)
              print(df.loc[i]["book_title"])
              print(score)
              list_sim.append((book_title,df.loc[i]["book_title"], score))
            #list_sim.append((book_title,df.loc[i]["book_title"] , doc1, doc2, list_docs[i][1],score))
      except:
          continue

    return list_sim



list_complete = []

for i in range(len(book_subset_NA)):
    try:
        list_docs = transformSpacy(book_subset_NA, i)
        df3 = calculateSimWithSpaCy(nlp, i, book_subset_NA, list_docs, str(book_subset_NA.loc[i]["book_desc"]),str(book_subset_NA.loc[i]["book_title"]), n=15)
        list_complete.append((df3))
    except:
        continue
    

synopsis_sim = pd.DataFrame(np.concatenate(list_complete), columns =["book_title","book_comp","sim_score"])
print(synopsis_sim.shape)

synopsis_sim.to_csv("synopsis_sim.csv")
