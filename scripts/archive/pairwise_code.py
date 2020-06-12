# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 11:05:12 2020

@author: Jothimani
"""

import pandas as pd 
import numpy as np 
from numpy import linalg as LA

# intialise data of lists.
data = {'Name':['Tom', 'nick', 'krish', 'jack'],
        'Age':[[20,20], [21,21], [19,19], [18,18]]}
 
# Create DataFrame
df = pd.DataFrame(data)
 
# Print the output.
print(df)

df1 = pd.DataFrame()
df1["book_title"] = ""
df1["book_comp"] = ""
df1["score"] = ""

columns = list(df1.columns)
data = []

for i in range(len(df['Name'])):
    print("i", i)
    for j in range(len(df['Name'])):
        print("j",j)
        if i != j: 
            diff = np.array(df.at[i, "Age"]) - np.array(df.at[j, "Age"])
            score = LA.norm(diff)
            first_column = df.at[i, "Name"]
            second_column = df.at[j, "Name"]
            values = [first_column, second_column, score]
            zipped = zip(columns, values)
            a_dictionary = dict(zipped)
            print(a_dictionary)
            data.append(a_dictionary)
    
        
    df1 = df1.append(data)
    df1.drop_duplicates(keep='last', inplace = True)
    print(df1)
        