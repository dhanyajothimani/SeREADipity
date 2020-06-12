# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 23:44:47 2020

@author: Jothimani
"""

import streamlit as st
import pandas as pd
import numpy as np

from sklearn import preprocessing


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

#def fxn():
#    warnings.warn("cache", CachedObjectMutationWarning)
#
#with warnings.catch_warnings():
#    warnings.simplefilter("ignore")
#    fxn()

'''
# Welcome to SeREADipity!

Pick a book you love- and the choices that guide your reading - and explore where the connections take you...
'''

#recommendation_data = st.cache(pd.read_csv)("consolidated_results.csv")

@st.cache(allow_output_mutation=True)
def load_data():
    df = pd.read_csv("consolidated_results.csv")
    return df

# Will only run once if already cached
recommendation_data1 = load_data()

user_input = st.text_input('I enjoyed reading:')
#st.write('The Entered URL is', url)

'''
Find me book that... 
'''

sim_imp = st.slider("have a similar plot: ", min_value=0, max_value=10, value=5, step=1)

years_imp = st.slider("have a similar writing style: ", min_value=0, max_value=10, value=5, step=1)

genre_imp = st.slider("are on similar topics", min_value=0, max_value=10, value=5, step=1)

award_imp = st.slider("are by award-winning authors: ", min_value=0, max_value=10, value=5, step=1)

recommendation_data = recommendation_data1.copy()

recommendation_data["final_score"] = ""


#recommendation_data.filter(regex=user_input)
is_book = recommendation_data['book_title']==user_input
recom_user =  recommendation_data[is_book]

#if is_book.empty or is_book.bool():
#    st.write(user_input," is not found in our database.")
#else:
#    recom_user = recommendation_data[is_book]

x = recom_user[['years']].values.astype(float)
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
recom_user["scaled_year"] = x_scaled

y = recom_user[['genre_sim']].values.astype(float)
min_max_scaler = preprocessing.MinMaxScaler()
y_scaled = min_max_scaler.fit_transform(y)
recom_user["scaled_genre"] = y_scaled



def final_score(df, award_imp, genre_imp, years_imp, sim_imp):
    df = df.reset_index()
    for i in range(df.shape[0]):
        print(i)
        df.at[i,"final_score"] = ((award_imp/10) * df.loc[i]["award"]) + ((genre_imp/10) * df.loc[i]["scaled_genre"])+((years_imp/10) * df.loc[i]["scaled_year"])+((sim_imp/10) * float(df.loc[i]["sim_score"]))
        print(df.at[i,"final_score"])
     
    return(df)
    
    
    
final_score_df = final_score(recom_user,award_imp, genre_imp, years_imp, sim_imp )
#print(final_score_df)

final_score_sorted = final_score_df.sort_values('final_score', ascending = False)
#print(final_score_sorted["book_comp"].head(10))
recom_books = final_score_sorted["book_comp"].head(10)
recom_books = recom_books.reset_index()
#recom_books.to_string(index=False)
'''
You may enjoy: 
'''
st.write("    1: ", recom_books.loc[0]["book_comp"])
st.write("    2: ", recom_books.loc[1]["book_comp"])
st.write("    3: ", recom_books.loc[2]["book_comp"])
st.write("    4: ", recom_books.loc[3]["book_comp"])
st.write("    5: ", recom_books.loc[4]["book_comp"])
st.write("    6: ", recom_books.loc[5]["book_comp"])
st.write("    7: ", recom_books.loc[6]["book_comp"])
st.write("    8: ", recom_books.loc[7]["book_comp"])
st.write("    9: ", recom_books.loc[8]["book_comp"])
st.write("   10: ", recom_books.loc[9]["book_comp"])





#'''
#© Dhanya Jothimani 2020 
#'''
