# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 16:43:35 2020

@author: Jothimani
"""

from bs4 import BeautifulSoup
import requests 
import pandas as pd
import re
from dateutil.parser import parse
import os 

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)


os.chdir("C:\\Users\\Jothimani\\Documents\\GR\\")

#Ref:https://stackoverflow.com/questions/18171739/unicodedecodeerror-when-reading-csv-file-in-pandas-with-python
author_database = pd.read_csv("author_database.csv",encoding = "ISO-8859-1", engine='python')
#author_database = pd.read_csv("sample_wiki_scraping.csv",encoding = "ISO-8859-1", engine='python')
author_database.shape

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
    
    born_dict = []
    died_dict = []
    award_dict = []
    lit_movement_dic = []
    
    for i in df["book_authors"]:
        try:
            print(i)
            soup = wikipedia_search(i)
            infobox = soup.find('table', class_='infobox vcard')
            if infobox is not None:
                born = infobox.find('th', text='Born')
                died = infobox.find('th', text='Died')
                awards = infobox.find('th', text='Notable awards')
                litmove = infobox.find('th', text='Literary movement')
            else:
                infovbox = soup.find('table', class_='infobox biography vcard') 
                if infovbox is not None:
                    born = infovbox.find('th', text='Born')
                    died = infovbox.find('th', text='Died')
                    awards = infovbox.find('th', text='Notable awards')
                    litmove = infovbox.find('th', text='Literary movement')
                    
            if born is None:
                born_dict.append("")
                print(born)
            else:
                born = born.next_sibling
                born = born.text.strip()
                born = re.search(r" (\d{4})", born).group(1)
                print(born)
                born_dict.append(born)
            
            if died is None:
                died_dict.append("2020")
                print(died)
            else: 
                died = died.next_sibling
                died = died.text.strip()
                died = re.search(r" (\d{4})", died).group(1)
                print(died)
                died_dict.append(died)
                #https://stackoverflow.com/questions/40121822/extracting-year-from-string-in-python
                
            if awards is None:
                award_dict.append("No award")
                print(awards)
            else: 
                awards = awards.next_sibling
                awards = awards.text.strip()
                award_dict.append(awards)
                print(awards)
        
            if litmove is None:
                lit_movement_dic.append("Data NA")
                print(litmove)
            else:
                litmove = litmove.next_sibling
                litmove = litmove.text.strip()
                lit_movement_dic.append(litmove)
                print(litmove)
    
                          
            
               
        except:
            born_dict.append("")
            died_dict.append("")
            award_dict.append("")
            lit_movement_dic.append("")
            continue 
        
    df["born"] = born_dict
    df["died"] = died_dict
    df["notable_award"] = award_dict
    df["lit_movement"] = lit_movement_dic
    return (df)

#author_database1 = author_database[:10]
auth_db = get_author(author_database)
auth_db.to_csv("author_database_updated.csv")


