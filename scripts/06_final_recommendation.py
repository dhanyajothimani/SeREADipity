# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 01:29:21 2020

@author: Jothimani
"""
import pandas as pd
import os 
from sklearn import preprocessing


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)


os.chdir("C:/Users/Jothimani/Documents/GR")

recommendation_data = pd.read_csv("consolidated_results.csv") 
recommendation_data.shape

user_input = "The Great Gatsby"
award_imp = 0
genre_imp = 0
years_imp = 10
sim_imp = 0

total_imp = award_imp + genre_imp + years_imp + sim_imp

award_weight = award_imp/total_imp
genre_weight = genre_imp/total_imp
years_weight = years_imp/total_imp
sim_weight = sim_imp/total_imp

recommendation_data["final_score"] = ""

#recommendation_data.filter(regex=user_input)

is_book = recommendation_data['book_title']==user_input
recom_user =  recommendation_data[is_book]

x = recom_user[['years']].values.astype(float)
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
recom_user["scaled_year"] = x_scaled
recom_user["year_sim"] = 1 - recom_user["scaled_year"]



def final_score(df, award_weight, genre_weight, years_weight, sim_weight):
    df = df.reset_index()
    for i in range(df.shape[0]):
        print(i)
        df.at[i,"final_score"] = (award_weight * df.loc[i]["award"]) + (genre_weight * df.loc[i]["genre_sim"])+(years_weight * df.loc[i]["year_sim"])+(sim_weight * float(df.loc[i]["sim_score"]))
        print(df.at[i,"final_score"])
     
    return(df)
    
    
    
final_score_df = final_score(recom_user,award_weight, genre_weight, years_weight, sim_weight )
print(final_score_df)

final_score_sorted = final_score_df.sort_values('final_score', ascending = False)
print(final_score_sorted["book_comp"].head(10))