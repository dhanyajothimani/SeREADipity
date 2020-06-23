# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 18:20:59 2020

@author: Jothimani
"""
import pandas as pd 
import numpy as np 
import os 

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

import spacy
nlp = spacy.load('en_core_web_md')

from numpy import linalg as LA

os.chdir("C:\\Users\\Jothimani\\Documents\\GR\\")


genre_db = pd.read_csv("genre_database.csv")



#Get unique genres from the dataset
def unique_values(df):
    
    unique_dict = pd.DataFrame()
    
    for i in range(df.shape[1]):
        try:
            for j in range(df.shape[1]):
                #print(i)
                print(str("genre")+str(j))
                if df.columns[i]== "genre"+str(j):
                    unique_dict = pd.concat([unique_dict, df["genre"+str(j)]])
                    print(unique_dict.head())
        except:
            continue
    
    unique_dict = unique_dict[0].unique()
     #Remove 
    cleaned_genre = [x for x in unique_dict if str(x) != 'nan']           
    return(cleaned_genre)
    
    
#Get the word embeddings for each genre
def genre_space(genre_list):
    vector_space = []
    
    for i in genre_list:
        try:
            doc = nlp(i)
            vector_space.append((i, doc.vector))
        except:
            continue
    vector_space = pd.DataFrame(vector_space)
    return(vector_space)

#Get unique genres
unique_genre = unique_values(genre_db)
print(len(unique_genre))

#Get the parameter space for all genres
genre_parameter = genre_space(unique_genre)
print(genre_parameter.shape)


#Finding the books in the genre parameter space
genre_parameter.head()
genre_parameter[0][0] #Young Adult
genre_parameter[0][1] #Fantasy
genre_parameter.shape #(253,2)
type(genre_parameter)

genre_parameter.rename(columns={ genre_parameter.columns[0]: "genre"}, inplace = True)
genre_parameter.rename(columns={ genre_parameter.columns[1]: "genre_value"}, inplace = True)


#Replace the genre with the genre vector embeddings for each book
def genre_vector(df, dict1):
    df1 =df.copy()
    for i in range(df1.shape[0]):
        try:
            print("Step1")
            for j in range(df1.shape[1]):
                print("Step2")
                for k,v in dict1.items():
                    print("Step3")
                    print(k)
                    if df1.loc[i][j] == str(k):
                        print("Step4")
                        print(v)
                        df1.iat[i, j] = v
                        #df.replace(to_replace = str(k), value = v)
        except:
            continue
    #print(df)
    return(df1)                
            
    
    
    
genre_db1 = genre_db.copy()

#https://stackoverflow.com/questions/18695605/python-pandas-dataframe-to-dictionary
gpd = genre_parameter.set_index('genre')['genre_value'].to_dict() 

book_genre_df = genre_vector((genre_db1.drop(["book_title"], axis =1)), gpd)
book_genre_df_test = genre_vector(genre_db1, gpd)

#for each book, obtain the genre vector embeddings by taking the weighted sum of vectors of all genres

def vector_sum(df, dict1):
    df1 = df.copy()
    print(df1.shape)
    x0 = 0
    sum_v = np.array ([x0*300])
    print(len(sum_v))
    n_col = (df1.shape[1])+1
    df1["n_col"] = ""
    print(df1.shape)
    print(n_col)
    for i in range(df1.shape[0]):
        try:
        #print("Step1")
            for j in range(df1.shape[1]):
             #   print("Step2")
                for k,v in dict1.items():
              #      print("Step3")
                    #print(k)
                    if df1.loc[i][j] == str(k):
                        print("Step4")
                        vT = v[np.newaxis]
                        print(len(vT))
                        sum_v = sum_v + vT
                        #print(sum_v)
                        print(len(sum_v))
                        print(type(sum_v))
                        df1.at[i, "n_col"] = list(sum_v)
        except:
            continue
                    
    
    print(df1.shape)
    return(df1) 

cumm_sum = vector_sum(genre_db1, gpd)       

cumm_sum["d_norm"]= [cumm_sum.loc[i]["n_col"]/LA.norm(cumm_sum.loc[i]["n_col"]) for i in range(cumm_sum.shape[0])]
                

#Obtaining the genre similarity of two books
def genre_diff(df, column_name):
    df1 = pd.DataFrame()
    df1["book_title"] = ""
    df1["book_comp"] = ""
    df1["genre_sim"] = ""
    
    columns = list(df1.columns)
    data = []
    
    for i in range(len(df[column_name])):
        try:
            print("i", i)
            for j in range(len(df[column_name])):
                print("j",j)
                if i != j: 
                    diff = np.array(df.at[i, column_name]) - np.array(df.at[j, column_name])
                    score = LA.norm(diff)
                    first_column = df.at[i, "book_title"]
                    second_column = df.at[j, "book_title"]
                    values = [first_column, second_column, score]
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

genre_dist = genre_diff(cumm_sum, "d_norm")
genre_dist.to_csv("genre_db.csv")

