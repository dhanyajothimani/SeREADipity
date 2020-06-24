# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 16:43:35 2020

@author: Jothimani
"""

from bs4 import BeautifulSoup
import requests 
import pandas as pd
import re
import os 

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)


os.chdir("C:\\Users\\Jothimani\\Documents\\GR\\")

#Ref:https://stackoverflow.com/questions/18171739/unicodedecodeerror-when-reading-csv-file-in-pandas-with-python
author_database1 = pd.read_csv("author_database.csv",encoding = "ISO-8859-1", engine='python')
print(author_database1.shape)

author_database = author_database1.dropna()
print(author_database.shape)

def wikipedia_search(subject, url=False):
    if url is False:
        response = requests.get('http://en.wikipedia.org/w/index.php',
                                params={'search':subject}
#                                headers={'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko)'})
                                )
    else :
        response = requests.get(url,
                                headers={'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko)'})
    soup = BeautifulSoup(response.text, "lxml")
    return soup


def get_author(df):
    
    df["born"] = ""
    df["died"] = ""
    df["lit_move"] = ""
    df["awards"] = ""
    
    for j in df.index:
        i = df.loc[j]["book_authors"]
        try:
            soup = wikipedia_search(i)
            infobox = soup.find('table', class_='infobox vcard')
            if infobox is not None:
                print(i)
                born = infobox.find('th', text='Born')
                died = infobox.find('th', text='Died')
                awards = infobox.find('th', text='Notable awards')
                litmove = infobox.find('th', text='Literary movement')
            else:
                print(i)
                infovbox = soup.find('table', class_='infobox biography vcard') 
                if infovbox is not None:
                    born = infovbox.find('th', text='Born')
                    died = infovbox.find('th', text='Died')
                    awards = infovbox.find('th', text='Notable awards')
                    litmove = infovbox.find('th', text='Literary movement')
                    
            if born is None:
                df.at[j, "born"] = ""
                print("NA")             
            else:
                born = born.next_sibling
                born = born.text.strip()
                born = re.search(r" (\d{4})", born).group(1)
                print(born)
                df.at[j,"born"] = born
            
            if died is None:
                df.at[j,"died"] = 2020
                print("NA")            
            else: 
                died = died.next_sibling
                died = died.text.strip()
                died = re.search(r" (\d{4})", died).group(1)
                print(died)
                df.at[j,"died"] = died
                #https://stackoverflow.com/questions/40121822/extracting-year-from-string-in-python
                
            if awards is None:
                df.at[j,"awards"] = "No award"
                print("No award")
            else: 
                awards = awards.next_sibling
                awards = awards.text.strip()
                df.at[j,"awards"] = awards
                print(awards)
        
            if litmove is None:
                df.at[j,"lit_move"] = "Data NA"
                print("Data NA")
            else:
                litmove = litmove.next_sibling
                litmove = litmove.text.strip()
                df.at[j,"lit_move"] = litmove
                print(litmove)
               
        except:
            print(i)
            continue 
    
    
    print(df.shape)
    return (df)


auth_db1 = get_author(author_database)
auth_db1.to_csv("author_database_updated.csv")
