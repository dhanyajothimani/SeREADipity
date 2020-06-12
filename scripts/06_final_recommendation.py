# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 01:29:21 2020

@author: Jothimani
"""

import pandas as pd
import os 
import numpy as np
from sklearn import preprocessing


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)


os.chdir("C:/Users/Jothimani/Documents/GR")

recommendation_data = pd.read_csv("consolidated_results.csv") 
recommendation_data.shape

user_input = "Gone with the Wind"
award_imp = 2
genre_imp = 9
years_imp = 0
sim_imp = 9 

recommendation_data["final_score"] = ""

#recommendation_data.filter(regex=user_input)

is_book = recommendation_data['book_title']==user_input
recom_user =  recommendation_data[is_book]

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
print(final_score_df)

final_score_sorted = final_score_df.sort_values('final_score', ascending = False)
print(final_score_sorted["book_comp"].head(10))




