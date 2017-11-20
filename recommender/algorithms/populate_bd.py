# -*- coding: utf-8 -*-

import pandas as pd
from recommender.models import Movie
import os


class PopulateBd:

    def populate_bd(self):
        directory = os.path.abspath(os.path.join("..", os.path.dirname(__file__)))
        movies = pd.read_csv(directory+'/data/movies.csv', quotechar='"', names=["url", "description", "rationale", "benefits", "problems", "objectives", "content", "title"])

        for mv in movies.itertuples():
            item = Movie.objects.create(movie_name=mv.title, movie_description=mv.description)
            item.rationale = mv.rationale
            item.benefits = mv.benefits
            item.problems = mv.problems
            item.objectives = mv.objectives
            item.save()

    # def __call__(self):
    #     print("Database populated!")
