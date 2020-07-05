Calculation of Similarity Metrics and Recommendation Engine
-------------------------------------------------

**01_synopsis_similarity.py**: Calculates the similarity between the books based on the synopsis using BERT and cosine similarity (scripts > archive > content_recommendation.py follows the NLP pipelines - (1a) count vectorizer, (1b) TF-IDF vectorizer, (1c) Word2Vec using Spacy and (2) calculates similarity using (a) cosine similarity and (b) k Nearest Neighbour)

**02_author_genre_extraction.py**: Extracts authors and genres of book in proper format into different columns for easy processing. 

**03_award_style_metrics.py**: For each author, calculates the literary award metric, and style similarity metric using years active data.

**04_genre_similarity.py**: Calculates the genre similarity for each book using BERT. 

**05_consolidation.py**: Compiles four metrics - synopis similarity, genre similarity, style similarity and award metric.

**06_final_recommendation.py**: Calculates the final similarity for book using all similarity metrics and user inputs, and recommends top 10 books.
