from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.urls import reverse

from .models import Movie, Learner, Rating, User

# Create your views here.

def index(request):
    movies = Movie.objects.order_by("movie_name")
    context = {'movie_list' : movies}
    return render(request, 'recommender/index.html', context)

def login(request):
    return HttpResponse("Esta é a página de login")

def new_user(request):
    return render(request, 'recommender/new_user.html')

def register(request):
    user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'], password=request.POST['password'])
    user.first_name=request.POST['firstname']
    user.last_name=request.POST['lastname']
    user.save()
    url = reverse('new_learner', kwargs={'user_id':user.pk})
    return HttpResponseRedirect(url)

def new_learner(request, user_id):
    user = User.objects.get(pk=user_id)
    context = {'user' : user}
    return render(request, 'recommender/new_learner.html', context)

def register_learner(request, user_id):
    learner = Learner.objects.create(user=User.objects.get(pk=user_id))
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
    url = reverse('login')
    return HttpResponseRedirect(url)

def preferences(request, user_id):
    return HttpResponse("Aqui o usuário %s dá notas a filmes que já assistiu" % user_id)

def recommendation(request, user_id):
    user = Learner.objects.get(pk=user_id)
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

def home(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        if user.is_active:
            login(user)
            url = reverse('recommendation', kwargs={'user_id': user.learner.pk})
            return HttpResponseRedirect(url)
        else:
            # Return a 'disabled account' error message
            return HttpResponse("This user account is not active!")
    else:
        # Return an 'invalid login' error message.
        return HttpResponse("Invalid username or password %s" % username)