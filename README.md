<kbd>
  <img src="https://github.com/dhanyajothimani/SeREADipity/blob/master/images/user_preferences.png">
</kbd>

## SeREADipity

SeREADipity is a personalised book recommendation system that allows the users to rate their preferences (on the scale of 1 to 10) on various criteria - synopsis, literary period, genre and book by an award-winning author. 

SeREADipity uses close to 9,000 books (after data cleaning) and corresponding author details from GoodReads and Wikipedia, respectively. 

For each criterion, the similarity metric is calculated. Synopsis and genre similarities are obtained using cosine similarity and BERT. Literary period similarity is calculated as a mathematical function based on the years in which the authors were active. Award metric is designated as a binary variable. Based on the user's preferences, SeREADipidity recommends 10 books based on overall similarity score. The overall similarity score is calculated as a linear function of synopsis similatiy, literary period similarity, genre similarity and award metric.  

More details on the pipeline can be found [here](https://docs.google.com/presentation/d/1MznAeNaxGhhwfCA7KLQ7lKF5eAKheXIELDOAXApF-ds/edit#slide=id.g892ebf7653_0_2660).

Following is the screenshot of the book recommendations for **The Origin of Species** based on similar genre and synopsis. 

<kbd>
  <img src="https://github.com/dhanyajothimani/SeREADipity/blob/master/images/recom_genre.png">
</kbd>

## Pre-requisites 
 
 * pandas==0.24.2
 * scikit_learn==0.23.1
 * streamlit==0.62.1

## To Run the App Locally 

To get the book recommendation locally on your machine, download the files from the folder /SeREADipity/sereadipity. Change the path to the correspoding location on your machine. 

On the terminal, use the command `streamlit run sereadipity.py` to get a recommendation similar to the book you enjoyed! :) 

### Acknowledgments

Many thanks to Niall, Chris and fellow Fellows at Insight for the continuous feedback starting from project ideation till final product. Also, a special thanks is due to Amma, Appa, Arjun, Papa and Mumma! :) 
