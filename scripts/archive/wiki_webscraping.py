# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 15:13:33 2020

@author: Jothimani
"""

from bs4 import BeautifulSoup
import requests 
import pandas as pd
import re
from dateutil.parser import parse


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


def get_author(i):
    author_rows = []
    author_dict = dict()
    
    soup = wikipedia_search(i)
    df = pd.DataFrame(columns=["author","born","genre","died"])
    
    
    
    infobox = soup.find('table', class_='infobox vcard')
    if infobox is not None:
        born = infobox.find('th', text='Born')
        if born is None:
            author_dict['birth_year'] = ""
            print(author_dict['birth_year'])
        else:
            born = born.next_sibling
            born = born.text.strip()
            print(born)
            author_dict['birth_year'] = re.search(r" (\d{4})", born).group(1)
            print(author_dict['birth_year'])
            
        genre = infobox.find('th', text='Genre')
        if genre is None:
            author_dict['genre_list'] = ""
            print(author_dict['genre_list'])
        else:
            genre = genre.next_sibling
            genre = (genre.text.strip())
            genre1 = str.split(genre, ',') or str.split(genre, '\n') or genre or str.split(genre, '.')
            author_dict['genre_list'] = '|'.join(genre1)
            print(author_dict['genre_list'])
            
        died = infobox.find('th', text='Died')
        if died is None:
            author_dict['death_year'] = "Present"
            print(author_dict['death_year'])
        else: 
            died = died.next_sibling
            died = died.text.strip()
            print(died)
            author_dict['death_year'] = re.search(r" (\d{4})", died).group(1)
            print(author_dict['death_year'])
            #https://stackoverflow.com/questions/40121822/extracting-year-from-string-in-python
            
        awards = infobox.find('th', text='Notable awards')
        if awards is None:
            author_dict['awards_list'] = ""
            print(author_dict['awards_list'])
        else: 
            awards = awards.next_sibling
            awards = awards.text.strip()
            awards1 = str.split(awards, ',') or str.split(awards, '\n') or awards or str.split(awards, '.')
            author_dict['awards_list'] = '|'.join(awards1)
            print(author_dict['awards_list'])
            
        litmove = infobox.find('th', text='Literary movement')
        if litmove is None:
            author_dict['litmove_list'] = ""
            print(author_dict['litmove_list'])
        else: 
            litmove = litmove.next_sibling
            litmove = litmove.text.strip()
            litmove1 = str.split(litmove, ',') or str.split(litmove, '\n') or litmove or str.split(litmove, '.') or str.split(litmove, ' ')
            author_dict['litmove_list'] = '|'.join(litmove1)
            print(author_dict['litmove_list'])
          
    else:
        infovbox = soup.find('table', class_='infobox biography vcard') 
        if infovbox is not None:
            born = infovbox.find('th', text='Born')
            if born is None:
                author_dict['birth_year'] = ""
                print(author_dict['birth_year'])
            else:
                born = born.next_sibling
                born = born.text.strip()
                print(born)
                author_dict['birth_year'] = re.search(r" (\d{4})", born).group(1)
                print(author_dict['birth_year'])
                
            genre = infovbox.find('th', text='Genre')
            if genre is None:
                author_dict['genre_list'] = ""
                print(author_dict['genre_list'])
            else:
                genre = genre.next_sibling
                genre = (genre.text.strip())
                genre1 = str.split(genre, ',') or str.split(genre, '\n') or genre or str.split(genre, '.')
                author_dict['genre_list'] = '|'.join(genre1)
                print(author_dict['genre_list'])
                
            died = infovbox.find('th', text='Died')
            if died is None:
                author_dict['death_year'] = "Present"
                print(author_dict['death_year'])
            else: 
                died = died.next_sibling
                died = died.text.strip()
                print(died)
                author_dict['death_year'] = re.search(r" (\d{4})", died).group(1)
                print(author_dict['death_year'])
                #https://stackoverflow.com/questions/40121822/extracting-year-from-string-in-python
                
            awards = infovbox.find('th', text='Notable awards')
            if awards is None:
                author_dict['awards_list'] = ""
                print(author_dict['awards_list'])
            else: 
                awards = awards.next_sibling
                awards = awards.text.strip()
                awards1 = str.split(awards, ',') or str.split(awards, '\n') or awards or str.split(awards, '.')
                author_dict['awards_list'] = '|'.join(awards1)
                print(author_dict['awards_list'])
                
            litmove = infovbox.find('th', text='Literary movement')
            if litmove is None:
                author_dict['litmove_list'] = ""
                print(author_dict['litmove_list'])
            else: 
                litmove = litmove.next_sibling
                litmove = litmove.text.strip()
                litmove1 = str.split(litmove, ',') or str.split(litmove, '\n') or litmove or str.split(litmove, '.') or str.split(litmove, ' ')
                author_dict['litmove_list'] = '|'.join(litmove1)
                print(author_dict['litmove_list'])
                
    author_rows.append(author_dict)
    print(author_rows)
    print(pd.DataFrame(author_rows))
    df = pd.DataFrame.from_dict(author_rows)
    print(df.shape)
    return(born, genre, died, awards, litmove)


author = ['Salman Rushdie','Gabriel García Márquez','Chetan Bhagat',
          'Malcolm Gladwell', 'Kalki Krishnamurthy','Harper Lee']
df = pd.DataFrame(columns=["author","born","genre","died"])
for i in author:
    print(i)
    born, genre, died, awards, litmove = get_author(i)
    print("Worked")
#    





