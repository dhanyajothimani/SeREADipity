# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 21:00:41 2020

@author: Jothimani
"""

import pandas as pd 
import numpy as np 
import os 

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

os.chdir("C:\\Users\\Jothimani\\Documents\\GR")

author = pd.read_csv(r"author_database_updated.csv")

author_db = author.copy()
author_db.columns

author_db["years_active"] = round((author_db["born"] + author_db["died"])/2, 0)



def year_active_diff(df, column_name):
    df1 = pd.DataFrame()
    df1["book_title"] = ""
    df1["book_comp"] = ""
    df1["years"] = ""
        
    columns = list(df1.columns)
    data = []
    
    for i in range(df.shape[0]):
        try:
            print("i", i)
            for j in range(df.shape[0]):
                print("j",j)
                if i != j: 
                    diff = df.at[i, column_name] - df.at[j, column_name]
                    first_column = df.at[i, "book_title"]
                    second_column = df.at[j, "book_title"]
                    #norm_diff = ((-((diff))**(1/2)) - 1)
                    norm_diff = abs((-((diff))**(1/2)) - 1)
                    values = [first_column, second_column, norm_diff]
                    zipped = zip(columns, values)
                    a_dictionary = dict(zipped)
                    print(a_dictionary)
                    data.append(a_dictionary)
        except:
            continue
                    
    df1 = df1.append(data)
    df2 = df1.drop_duplicates(keep='last')
    print(df2)
    return(df2) 

year_db = year_active_diff(author_db, "years_active")   
year_db.to_csv("years_active.csv")



def award_fn(df, column_name):
    df["award"] =""
    for i in range(len(df[column_name])):
        try:
            val = df.loc[i, column_name]
            if val == "No award":
                df.loc[i,"award"] = 0
            else:
                df.loc[i,"award"] = 1
        except:
            continue
    return(df)
    
author_db_award = award_fn(author_db, "notable_award")
author_db_award.head()


def award_pair(df, column_name):
    df1 = pd.DataFrame()
    df1["book_title"] = ""
    df1["book_comp"] = ""
    df1["award"] = ""
    
    columns = list(df1.columns)
    data = []
    
    for i in range(df.shape[0]):
        try:
            print("i", i)
            for j in range(df.shape[0]):
                print("j",j)
                if i != j: 
                    award_value = df.at[j, column_name]
                    first_column = df.at[i, "book_title"]
                    second_column = df.at[j, "book_title"]
                    values = [first_column, second_column, award_value]
                    zipped = zip(columns, values)
                    a_dictionary = dict(zipped)
                    print(a_dictionary)
                    data.append(a_dictionary)
        except:
            continue
                    
    df1 = df1.append(data)
    df2 = df1.drop_duplicates(keep='last')
    print(df2)
    return(df2) 
        
author_db_award_pair = award_pair(author_db_award, "award")
author_db_award_pair.to_csv("awards.csv")
