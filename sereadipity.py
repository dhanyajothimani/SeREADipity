# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 23:44:47 2020

@author: Jothimani
"""

#Ref: https://medium.com/analytics-vidhya/how-to-deploy-a-streamlit-app-with-heroku-5f76a809ec2e

import streamlit as st
import pandas as pd
import sklearn
import torch
from pathlib import Path
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

### Pick a book you love- and the choices that guide your reading - and explore where the connections take you...
'''


#https://drive.google.com/uc?export=download&id=1Vme3VrkpygIJjPttPJh5_0aDCjbCL81H

#recommendation_data = st.cache(pd.read_csv)("consolidated_results.csv")
path = 'https://drive.google.com/u/0/uc?export=download&confirm=nnwJ&id=1Vme3VrkpygIJjPttPJh5_0aDCjbCL81H'


# Hosted on my personal account until I figure something else out
cloud_model_location = "1Vme3VrkpygIJjPttPJh5_0aDCjbCL81H"
# Streamlit sharing is CPU only
device = torch.device('cpu')
#@st.cache(suppress_st_warning=True)
@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def load_data():

    save_dest = Path('model')
    save_dest.mkdir(exist_ok=True)

    f_checkpoint = Path("model/consolidated_results.csv")

    if not f_checkpoint.exists():
        with st.spinner("Downloading data... this may take awhile! \n Don't stop it!"):
            from GD_download import download_file_from_google_drive
            download_file_from_google_drive(cloud_model_location, f_checkpoint)

    model = torch.load(f_checkpoint, map_location=device)
    st.write(model.head())
    model.eval()
    return model


# Will only run once if already cached
# can be used once streamlit has git lfs access
recommendation_data1 = load_data()
st.write(recommendation_data1.head())

#recommendation_data1.columns = recommendation_data1.columns.str.strip()

#st.write(recommendation_data1.columns)
#st.write(recommendation_data1.head(5))

cols = recommendation_data1.book_title.unique()
options = list(cols)


user_input = st.multiselect("I enjoyed reading:", options = options, default= options[100:101])


'''
### Find me books that...
'''

sim_imp = st.slider("have a similar plot: ", min_value=0, max_value=10, value=5, step=1)

years_imp = st.slider("are from similar literary period: ", min_value=0, max_value=10, value=5, step=1)

genre_imp = st.slider("are on similar topics", min_value=0, max_value=10, value=5, step=1)

award_imp = st.slider("are by award-winning authors: ", min_value=0, max_value=10, value=5, step=1)

recommendation_data = recommendation_data1.copy()

recommendation_data["final_score"] = ""


is_book = recommendation_data['book_title']==user_input[0]
recom_user =  recommendation_data[is_book]

x = recom_user[['years']].values.astype(float)
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
recom_user["scaled_year"] = x_scaled
#max_x = max(x)
#recom_user["scaled_year"] = [i/max_x for i in x]
recom_user["year_sim"] = 1 - recom_user["scaled_year"]
recom_user["genre_sim_new"] = 1 - recom_user["genre_sim"]

recom_user["year_sim"] = recom_user["year_sim"].fillna(0)
recom_user["award"] = recom_user["award"].fillna(0)
recom_user["genre_sim_new"] = recom_user["genre_sim_new"].fillna(0)
recom_user["synopsis_sim"] = recom_user["synopsis_sim"].fillna(0)



def final_score(df, award_imp, genre_imp, years_imp, sim_imp):
    df = df.reset_index()
    for i in range(df.shape[0]):
        print(i)
        df.at[i,"final_score"] = (award_imp * df.loc[i]["award"]) + (genre_imp * df.loc[i]["genre_sim_new"])+(years_imp * df.loc[i]["year_sim"])+(sim_imp * float(df.loc[i]["synopsis_sim"]))
        print(df.at[i,"final_score"])

    return(df)


total_imp = (award_imp + genre_imp + years_imp + sim_imp)
award_imp = award_imp/total_imp
genre_imp = genre_imp/total_imp
years_imp = years_imp/total_imp
sim_imp = sim_imp/total_imp

final_score_df = final_score(recom_user,award_imp, genre_imp, years_imp, sim_imp )
#print(final_score_df)

final_score_sorted = final_score_df.sort_values('final_score', ascending = False)
#print(final_score_sorted["book_comp"].head(10))
recom_books = final_score_sorted["book_comp"].head(10)
recom_books = recom_books.reset_index()
#recom_books.to_string(index=False)


st.write("Weights used in the recommendation algorithm for similar plots, literary period, topics, and award-winning authors:", round(sim_imp,2),",", round(years_imp,2),",", round(genre_imp,2),", and", round(award_imp,2))


'''
### You may enjoy:
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





'''
##### © Dhanya Jothimani 2020
'''
