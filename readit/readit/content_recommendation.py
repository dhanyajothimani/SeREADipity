# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 00:32:49 2020

@author: Jothimani
"""

import pandas as pd
import os 
import nltk
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
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

books_db = pd.read_csv(r"book_data_bk.csv")
books_db.head()
books_db.shape
book_db = books_db.drop_duplicates(keep = 'first', inplace = False)
book_db.shape

book_db.columns

book_subset = book_db[['book_title','book_authors','book_desc']]
book_subset.shape

book_subset.isnull().values.any()

book_subset_NA = book_subset.dropna()
book_subset_NA.isnull().values.any()

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

u = 'The Great Gatsby'
#u = 'Love in the Time of Cholera'
index = np.where(book_subset_NA['book_title'] == u)[0][0]
user_q = book_subset_NA.iloc[[index]]
user_q

book_subset_NA = book_subset_NA.drop(index)

#initializing tfidf vectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer()

#tfidf_book_desc = tfidf_vectorizer.fit_transform((book_subset_NA['book_desc'].values.astype('U'))) #fitting and transforming the vector
tfidf_book_desc = tfidf_vectorizer.fit_transform((book_subset_NA['book_desc'])) #fitting and transforming the vector
tfidf_book_desc

user_tfidf = tfidf_vectorizer.transform(user_q['book_desc'])

#Cosine similarity using TF-IDF
cos_similarity_tfidf = map(lambda x: cosine_similarity(user_tfidf, x, dense_output = True),tfidf_book_desc)

output2 = list(cos_similarity_tfidf)


def get_recommendation(top, df_all, scores):
  recommendation = pd.DataFrame(columns = ['Title',  'Author', 'score'])
  count = 0
  for i in top:
      #recommendation.at[count, 'Given Book'] = u
      recommendation.at[count, 'Title'] = df_all['book_title'][i]
      recommendation.at[count, 'Author'] = df_all['book_authors'][i]
      recommendation.at[count, 'score'] =  scores[count]
      count += 1
  return recommendation



#Top recommendations using TF-IDF
top = sorted(range(len(output2)), key=lambda i: output2[i], reverse=True)[:10]
list_scores = [output2[i][0][0] for i in top]
print("Cosine Similarity - TFIDF")
print(get_recommendation(top,book_subset_NA, list_scores))


#Count Vectorizer
count_vectorizer = CountVectorizer()

count_book_desc = count_vectorizer.fit_transform((book_subset_NA['book_desc'])) #fitting and transforming the vector
count_book_desc


user_count = count_vectorizer.transform(user_q['book_desc'])
cos_similarity_countv = map(lambda x: cosine_similarity(user_count, x),count_book_desc)

output2 = list(cos_similarity_countv)

top = sorted(range(len(output2)), key=lambda i: output2[i], reverse=True)[:10]
list_scores = [output2[i][0][0] for i in top]
print("Cosine Similarity - CV")
print(get_recommendation(top, book_subset_NA, list_scores))

#Recommendation Using Spacy 
#Transform the corpus of text to the Spacy's documents 
import time 
time.perf_counter()
list_docs = []
for i in range(len(book_subset_NA)):
    try:
        if i != index:
            doc = nlp("u'" + book_subset_NA['book_desc'][i] + "'")
            list_docs.append((doc,i))
        else:
            continue
    except:
        continue
print(len(list_docs))




def calculateSimWithSpaCy(nlp, df, user_text, n=6):
    # Calculate similarity using spaCy
    list_sim =[]
    doc1 = nlp("u'" + user_text + "'")
    for i in df.index:
      try:
            doc2 = list_docs[i][0]
            score = doc1.similarity(doc2)
            list_sim.append((doc1, doc2, list_docs[i][1],score))
      except:
        continue

    return list_sim

df3 = calculateSimWithSpaCy(nlp, book_subset_NA, str(user_q.book_desc), n=15)

df_recom_spacy = pd.DataFrame(df3).sort_values([3], ascending=False).head(10)
df_recom_spacy.reset_index(inplace=True)

index_spacy = df_recom_spacy[2]
list_scores = df_recom_spacy[3]

print("Spacy")
print(get_recommendation(index_spacy, book_subset_NA, list_scores))

#Using kNN
from sklearn.neighbors import NearestNeighbors
n_neighbors = 11
KNN = NearestNeighbors(n_neighbors, p=2)
KNN.fit(tfidf_book_desc)
NNs = KNN.kneighbors(user_tfidf, return_distance=True)

NNs[0][0][1:]

top = NNs[1][0][1:]
index_score = NNs[0][0][1:]

print("kNN")
print(get_recommendation(top, book_subset_NA, index_score))
