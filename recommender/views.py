# -*- coding: utf-8 -*-
# import os
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ALGORITHMS = os.path.join(BASE_DIR, '/recommender/algorithms')
#
# import sys
# sys.path.insert(0, ALGORITHMS)

import random
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .algorithms.populate_bd import PopulateBd
from .algorithms.content_similarity import ContentSimilarity
from django.db import IntegrityError
from .algorithms.sgd import FactMatrix

from .models import Movie, Learner, Rating, User


# @login_required
def index(request):
    if Movie.objects.all().count() == 0:
        pop = PopulateBd()
        pop.populate_bd()
        return HttpResponse("Populou!")
    movies = Movie.objects.order_by("movie_name")
    context = {'movie_list' : movies}
    return render(request, 'recommender/index.html', context)


def new_user(request):
    return render(request, 'recommender/new_user.html')

def register(request):
    try:
        user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'])
        user.first_name=request.POST['firstname']
        user.last_name=request.POST['lastname']
        user.save()
    except IntegrityError:
        return HttpResponse('User already exists!')
    return HttpResponseRedirect('/login/')

@login_required
def new_learner(request, user_id):
    user = User.objects.get(pk=user_id)
    context = {'user' : user}
    return render(request, 'recommender/new_learner.html', context)

@login_required
def register_learner(request, user_id):
    try:
        learner = Learner.objects.create(user_fk=User.objects.get(pk=user_id))
        learner.user_age = request.POST['user_age']
        learner.level_of_education = request.POST['level_of_education']
        learner.level_of_english = request.POST['level_of_english']
        learner.level_of_literature = request.POST['level_of_literature']
        learner.level_of_history = request.POST['level_of_history']
        learner.level_of_biology = request.POST['level_of_biology']
        learner.level_of_physics = request.POST['level_of_physics']
        learner.level_of_math = request.POST['level_of_math']
        learner.learning_goal = request.POST['learning_goal']
        learner.learning_style = request.POST['learning_style']
        learner.save()
        url = reverse('preferences', kwargs={'learner_id': learner.pk})
        return HttpResponseRedirect(url)
    except IntegrityError:
        HttpResponse('Learner already exists!')

@login_required
def preferences(request, learner_id):
    num_movies = Movie.objects.all().count()
    rand_movies = random.sample(range(num_movies), 20) #select 20 ids randomly
    movies = Movie.objects.filter(id__in=rand_movies) #filter the set of movies to be between such random ids
    learner = Learner.objects.get(pk=learner_id)
    user = User.objects.get(pk=learner.user_fk_id) #get the user from the learner_id

    context = {'movie_list': movies,
               'user': user,
               'learner': learner}
    return render(request, 'recommender/preferences.html', context)

@login_required
def register_preferences(request, learner_id):
    learner = Learner.objects.get(pk=learner_id)
    learner_movie_set = learner.rating_set.all()
    rated_movies = list(request.POST.items())

    if learner_movie_set.count() == 0:
        for key, value in rated_movies:
            if key == 'csrfmiddlewaretoken':
                continue #passes to the next iteration
            else:
                rating = Rating.objects.create(learner=learner, movie=Movie.objects.get(pk=key))
                rating.rating = int(value)
                rating.save()
        url = reverse('recommendation', kwargs={'learner_id': learner_id})
        return HttpResponseRedirect(url)
    else:
        for key, value in rated_movies:
            if key == 'csrfmiddlewaretoken':
                continue #passes to the next iteration
            else:
                rating = Rating.objects.get(movie=key, learner=learner_id)
                rating.rating = int(value)
                rating.context_time = datetime.now()
                rating.save()
        url = reverse('recommendation', kwargs={'learner_id': learner_id})
        return HttpResponseRedirect(url)

@login_required
def recommendation(request, learner_id): #Integrar algoritmo de fatoração de matrizes
    learner = Learner.objects.get(pk=learner_id)
    rated_movies = learner.rating_set.order_by('-predicted_rating') #get the set of movies ordered by user predicted rating

    if rated_movies.count() < Movie.objects.all().count(): #checks if the prediction algorithm has alredy been executed for this user
        url = reverse('populate_ratings', kwargs={'learner_id': learner_id})
        return HttpResponseRedirect(url)

    list_recommended_movies = []
    list_seen_movies = []
    for mv in rated_movies:
        if mv.rating is None: #selects only the movies the user has not rated (seen) yet
            list_recommended_movies.append((Movie.objects.get(pk=mv.movie_id), mv))
        else:
            list_seen_movies.append((Movie.objects.get(pk=mv.movie_id), mv))

    context = {'list_recommended_movies' : list_recommended_movies,
               'list_seen_movies' : list_seen_movies,
               'user' : request.user,
               'learner' : learner,}
    return render(request, 'recommender/recommendations.html', context)

def get_ratings(request, learner_id):
    context = {'learner_id': learner_id
               }
    return render(request, 'recommender/populate_ratings.html', context)

def populate_ratings(request, learner_id): #proposta de melhoria -> atualizar somente as notas do aprendiz de interesse (learner_id)
    fm = FactMatrix()
    R_hat = fm.sgd()
    usr = int(learner_id)

    # for usr in range(1, R_hat.shape[0]):
    for item in range(1, R_hat.shape[1]):

        learner = Learner.objects.filter(pk=usr)
        movie = Movie.objects.filter(pk=item)

        if learner.count() > 0 and movie.count() > 0:
            rating = Rating.objects.filter(learner=learner, movie=movie) #try to retrieve the rating object

            if rating.count() == 0: #check if the rating already exists
                rating = Rating.objects.create(learner=Learner.objects.get(pk=usr), movie=Movie.objects.get(pk=item))
                rating.predicted_rating = R_hat.loc[usr, item]
                rating.save()
            else:
                rating.predicted_rating = R_hat.loc[usr, item]
        elif learner.count() == 0:
            break
    url = reverse('recommendation', kwargs={'learner_id': learner_id})
    return HttpResponseRedirect(url)


@login_required
def movie_detail(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    ls = ContentSimilarity()
    list_similar_movies = ls.content_similarity(movie_id)
    context = {'movie' : movie,
               'list_similar_movies' : list_similar_movies}
    return render(request, 'recommender/movie_details.html', context)

def home(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            num_results = Learner.objects.filter(user_fk=user).count()
            if num_results > 0: #check if the user hasn't already filled out the learner form
                if Rating.objects.filter(learner=user.learner).count() > 0: #check if the learner has already rated any movies
                    url = reverse('recommendation', kwargs={'learner_id': user.learner.pk})
                else:
                    url = reverse('preferences', kwargs={'learner_id': user.learner.pk})
                return HttpResponseRedirect(url)
            else:
                url = reverse('new_learner', kwargs={'user_id': user.pk})
                return HttpResponseRedirect(url)
        else:
            # Return a 'disabled account' error message
            return HttpResponse("This user account is not active!")
    else:
        # Return an 'invalid login' error message.
        return HttpResponse("Invalid username or password")


def logout_view(request):
    logout(request)
    url = reverse('login')
    return HttpResponseRedirect(url)