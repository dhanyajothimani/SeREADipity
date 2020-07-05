# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 01:01:49 2020

@author: Jothimani
"""

import pandas as pd
import os 
import numpy as np
from functools import reduce


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)


os.chdir("C:/Users/Jothimani/Documents/GR")

awards = pd.read_csv("awards.csv") 
genre = pd.read_csv("genre_db.csv")
style = pd.read_csv("years_active.csv")
synopsis = pd.read_csv("synopsis_sim.csv")

#Ref: https://stackoverflow.com/questions/44327999/python-pandas-merge-multiple-dataframes
data_frames = [awards, genre, style, synopsis]

consolidated_results = reduce(lambda  left,right: pd.merge(left,right,on=['book_title', 'book_comp'],
                                            how='outer'), data_frames)

# if you want to fill the values that don't exist in the lines of merged dataframe simply fill with required strings as

#consolidated_results = reduce(lambda  left,right: pd.merge(left,right,on=['book_title', 'book_comp'],
#                                            how='outer'), data_frames).fillna(0)

consolidated_results = consolidated_results[["book_title", "book_comp", "award", "genre_sim", "years", "sim_score"]]

consolidated_results.to_csv("consolidated_results.csv")

