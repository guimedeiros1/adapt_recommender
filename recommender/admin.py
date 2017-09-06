from django.contrib import admin
from .models import Learner, Movie, Rating, User
# Register your models here.

admin.site.register(User)
admin.site.register(Learner)
admin.site.register(Movie)
admin.site.register(Rating)