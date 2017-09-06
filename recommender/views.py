from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

from .models import Movie, User, Rating

# Create your views here.

def index(request):
    movies = Movie.objects.order_by("movie_name")
    context = {'movie_list' : movies}
    return render(request, 'recommender/index.html', context)

def login(request):
    return HttpResponse("Esta é a página de login")

def register(request):
    return HttpResponse("Esta é a página de cadastro do usuário")

def preferences(request, user_id):
    return HttpResponse("Aqui o usuário %s dá notas a filmes que já assistiu" % user_id)

def recommendation(request, user_id):
    user = User.objects.get(pk=user_id)
    rated_movies = user.rating_set.order_by('predicted_rating') #get the set of movies ordered by user predicted rating
    list_recommended_movies = []
    for mv in rated_movies:
        if mv.rating == None: #selects only the movies the user has not rated (seen) yet
            list_recommended_movies.append(Movie.objects.get(pk=mv.movie_id))

    context = {'list_recommended_movies' : list_recommended_movies,
               'user' : user}
    return render(request, 'recommender/recommendations.html', context)

def movie_detail(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    context = {'movie' : movie}
    return render(request, 'recommender/movie_details.html', context)