import random
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime

from .models import Movie, Learner, Rating, User

# Create your views here.

def index(request):
    movies = Movie.objects.order_by("movie_name")
    context = {'movie_list' : movies}
    return render(request, 'recommender/index.html', context)

# def login(request):
#     return HttpResponse("Esta é a página de login")

def new_user(request):
    return render(request, 'recommender/new_user.html')

def register(request):
    user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'])
    user.first_name=request.POST['firstname']
    user.last_name=request.POST['lastname']
    user.save()
    return HttpResponseRedirect('/login/')

def new_learner(request, user_id):
    if request.user.is_authenticated():
        user = User.objects.get(pk=user_id)
        context = {'user' : user}
        return render(request, 'recommender/new_learner.html', context)
    else:
        return HttpResponse("User must be logged to see this page!")

def register_learner(request, user_id):
    if request.user.is_authenticated():
        learner = Learner.objects.create(user_fk=User.objects.get(pk=user_id))
        # learner.user = user_id
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
    else:
        return HttpResponse("User must be logged to see this page!")

def preferences(request, learner_id):
    if request.user.is_authenticated():
        # num_movies = Movie.objects.all().count()
        # rand_movies = random.sample(range(num_movies), 2)
        movies = Movie.objects.order_by('movie_name')
        learner = Learner.objects.get(pk=learner_id)
        user = User.objects.get(pk=learner.user_fk_id) #get the user from the learner_id
        context = {'movie_list': movies,
                   'user': user,
                   'learner': learner}
        # url = reverse('preferences', kwargs={'user_id':user_id})
        return render(request, 'recommender/preferences.html', context)
    else:
        return HttpResponse("User must be logged to see this page!")

def recommendation(request, learner_id):
    if request.user.is_authenticated():
        learner = Learner.objects.get(pk=learner_id)
        rated_movies = learner.rating_set.order_by('predicted_rating') #get the set of movies ordered by user predicted rating
        list_recommended_movies = []
        for mv in rated_movies:
            if mv.rating == None: #selects only the movies the user has not rated (seen) yet
                list_recommended_movies.append(Movie.objects.get(pk=mv.movie_id))

        context = {'list_recommended_movies' : list_recommended_movies,
                   'user' : request.user}
        return render(request, 'recommender/recommendations.html', context)
    else:
        return HttpResponse("User must be logged to see this page!")

def movie_detail(request, movie_id):
    if request.user.is_authenticated():
        movie = Movie.objects.get(pk=movie_id)
        context = {'movie' : movie}
        return render(request, 'recommender/movie_details.html', context)
    else:
        return HttpResponse("User must be logged to see this page!")

def home(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            num_results = Learner.objects.filter(user_fk=user).count()
            if num_results > 0: #verifies if the user has already setted a learner foreign key
                url = reverse('recommendation', kwargs={'learner_id': user.learner.pk})
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

def register_preferences(request, learner_id):
    if request.user.is_authenticated():
        learner = Learner.objects.get(pk=learner_id)
        learner_movie_set = learner.rating_set.all()
        rated_movies = list(request.POST.items())

        if learner_movie_set.count() == 0:
            for key, value in rated_movies[1:]: #skip first element because it is user token information
                rating = Rating.objects.create(learner=learner, movie=Movie.objects.get(pk=key))
                rating.rating = int(value)
                rating.save()
            url = reverse('recommendation', kwargs={'learner_id': learner_id})
            return HttpResponseRedirect(url)
        else:
            for key, value in rated_movies[1:]:  # skip first element because it is user token information
                rating = Rating.objects.get(movie=key, learner=learner_id)
                rating.rating = int(value)
                rating.context_time = datetime.now()
                rating.save()
            url = reverse('recommendation', kwargs={'learner_id': learner_id})
            return HttpResponseRedirect(url)
    else:
       return HttpResponse("User must be logged to see this page!")