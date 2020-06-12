# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 17:48:37 2020

@author: Jothimani
"""

import pandas as pd
import os 

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)


os.chdir("C:\\Users\\Jothimani\\Documents\\GR\\")

#Ref:https://stackoverflow.com/questions/18171739/unicodedecodeerror-when-reading-csv-file-in-pandas-with-python
book_database = pd.read_csv("book_data_bk.csv",encoding = "ISO-8859-1", engine='python')
print(book_database.shape)

print(book_database.head())

author_database = pd.DataFrame()
author_database = book_database[["book_title","book_authors"]]
author_database.shape

def author_split(df, column_name):
    
    word_dict = []
    for i in df[column_name]:
        try:
            print(i)
            word_split = i.split('|')
            word_dict.append(word_split[0])
        except:
            continue
    
    df[column_name] = word_dict
    print(df.head())
    return(df)

author_db = author_database
author_db1 = author_split(author_db, "book_authors")
author_db1.head()
author_db1.to_csv("author_database.csv")

def genre_split(df, column_name):
    
    word_dict = []
    for i in df[column_name]:
        try:
            print(i)
            word_split = i.split('|')
            word_dict.append(word_split)
        except:
            continue
    
    df[column_name] = word_dict
    print(len(word_dict))
    df1 = pd.DataFrame(word_dict)
    #print(df1)
    df3 = df.join(df1,how = "inner" )
    print(df3.shape)
    #print(df3.head())
    return(df3)



def rename_cols(df):
    col_names = list(df.columns)
    for i in range(len(col_names)):
        try:
            for j in range(len(col_names)):
                #print(df.columns[i])
                if df.columns[i] == j:
                    #print("Step2")
                    df.rename(columns = {j:"genre"+str(j)}, inplace = True)
        except:
            continue
                
    return(df)
    


genre_db = book_database[["book_title", "genres"]]
genre_db.head()
genre_db1 = genre_split(genre_db, "genres")
genre_db2 = genre_db1.drop("genres", axis = 1)
genre_db3 = rename_cols(genre_db2) 

print(genre_db3.columns)

genre_db3.to_csv("genre_database.csv")



