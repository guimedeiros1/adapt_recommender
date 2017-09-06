from django.conf.urls import url

from . import views

urlpatterns = [
    #ex: /recommender/
    url(r'^$', views.index, name='index'),
    # ex: /recommender/login/
    url(r'^login/$', views.login, name='login'),
    # ex: /recommender/register/
    url(r'^register/$', views.register, name='register'),
    # ex: /recommender/5/preferences
    url(r'^(?P<user_id>[0-9]+)/preferences/$', views.preferences, name='preferences'),
    # ex: /recommender/5/recommendation/
    url(r'^(?P<user_id>[0-9]+)/recommendation/$', views.recommendation, name='recommendation'),
    # ex: /recommender/5/movie_detail/
    url(r'^(?P<movie_id>[0-9]+)/movie_detail/$', views.movie_detail, name='recommendation'),
]