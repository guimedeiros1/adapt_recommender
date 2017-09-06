
# coding: utf-8

# ## First job: load the csv file and compute the tf-idf matrix

# In[14]:

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

#load csv to a pd DataFrame
movies = pd.read_csv('./data/movies.csv', quotechar='"', names=["url", "description", "rationale", "benefits", "problems", "objectives", "content", "title"])

movies.shape


# In[15]:

#model instantiation
vectorizer = TfidfVectorizer(min_df=1) 

#tokenize and compute tf-idf weights
tfidf = vectorizer.fit_transform(movies.content)


# ## Second job: Compute the cosine similarity between each video and select the most similar ones

# In[16]:

from sklearn.metrics.pairwise import cosine_similarity

#compute the similarity between movies 
similar = cosine_similarity(tfidf) 

#take the top-k most similar movies
most_similar = similar.argsort()[:,::-1][:,:6]


# In[18]:

most_similar


# ## Third job: return the most similar videos

# In[27]:

movie_id = 152


# In[28]:

print("The most similar videos are:")

#print the top-k movies
for i in range (0,most_similar.shape[1]):
    print ("Name: %s" %movies.title.iloc[most_similar[movie_id,i]])
    print ("Cosine similarity score: %f \n" %similar[movie_id,most_similar[movie_id,i]])


# In[ ]:



