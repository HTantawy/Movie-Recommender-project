# -*- coding: utf-8 -*-
"""Movie Recommendation model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wLJEONzk1wGh_wFkWpEtNYoQEcdgNg0r
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

movies = pd.read_csv('dataset.csv')

movies.head()

movies.columns

movies.info()

movies['combined_features'] = movies['title'] + ' ' + movies['genre'] + ' ' + movies['original_language'] + ' ' + movies['overview']
movies['combined_features'] = movies['combined_features'].fillna('')

movies.head()

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['combined_features'])

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

with open('cosine_sim.pkl', 'wb') as f:
    pickle.dump(cosine_sim, f)

print("Data Preprocessing and Similarity Calculation Complete")

def recommend(movie_title):
    try:
        idx = movies[movies['title'] == movie_title].index[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        movie_indices = [i[0] for i in sim_scores[1:11]]
        recommendations = movies['title'].iloc[movie_indices].to_list()
        return recommendations
    except IndexError:
        return ["Movie not found. Please try another title."]

print(recommend ("The Godfather"))

from google.colab import drive
drive.mount('/content/drive')



# Save the dataset and similarity matrix to disk
import pickle
import zipfile

# Save the cosine similarity matrix to a .pkl file
with open('cosine_sim.pkl', 'wb') as f:
    pickle.dump(cosine_sim, f)

# Compress the .pkl file into a zip file
with zipfile.ZipFile('cosine_sim.zip', 'w') as zipf:
    zipf.write('cosine_sim.pkl')

# Download the zip file
from google.colab import files
files.download('cosine_sim.zip')

import os

file_size = os.path.getsize('cosine_sim.pkl')
print(f"File size: {file_size / (1024 * 1024):.2f} MB")