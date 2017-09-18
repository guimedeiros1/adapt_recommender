import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from recommender.models import Movie

class ContentSimilarity:
    # MELHORIA FUTURA: SALVAR MOST SIMILAR NO BD E ATUALIZAR SOMENTE QDO NECESSÁRIO
    def content_similarity(self, movie_id):
        #transform the Movie QuerySet into a pandas DataFrame
        movies = pd.DataFrame(list(Movie.objects.all().values()))

        #model instantiation
        vectorizer = TfidfVectorizer(min_df=1)

        #tokenize and compute tf-idf weights
        tfidf = vectorizer.fit_transform(movies.movie_description)

        #compute the similarity between movies
        similar = cosine_similarity(tfidf)

        #take the top-5 most similar movies
        most_similar = similar.argsort()[:,::-1][:,:6]

        most_similar = pd.DataFrame(most_similar)

        list_similar_movies = []

        #make a list of top-k recommended movies
        for i in range (1,most_similar.shape[1]):
            sim_movie_id = most_similar.iloc[int(movie_id),i]
            list_similar_movies.append(Movie.objects.get(pk=sim_movie_id))
            # print ("Name: %s" %movies.title.iloc[most_similar[movie_id,i]])
            # print ("Cosine similarity score: %f \n" %similar[movie_id,most_similar[movie_id,i]])
        return list_similar_movies

    # def __call__(movie_id):
    #     print ('called')