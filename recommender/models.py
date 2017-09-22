from django.db import models
from django.contrib.auth.models import AbstractUser
from time import strftime
from datetime import datetime

# Create your models here.

class User(AbstractUser):
    pass
    def __str__(self):
        return 'Id - %s - Name - %s' % (self.id, self.username)

class Learner(models.Model):
    user_fk = models.OneToOneField(User, on_delete=models.CASCADE)
    learner_age = models.IntegerField(null=True, blank=True)

    FUNDAMENTAL = "EF"
    MEDIO = "EM"
    SUPERIOR = "ES"
    MESTRE = "MT"
    PHD = "DT"

    LEVELS_OF_EDUCATION_CHOICES = (
        (FUNDAMENTAL, "Ensino Fundamental"),
        (MEDIO, "Ensino Médio"),
        (SUPERIOR, "Ensino Superior"),
        (MESTRE, "Mestrado"),
        (PHD, "Doutorado"),
    )

    level_of_education = models.CharField(max_length=2,
                                          choices=LEVELS_OF_EDUCATION_CHOICES,
                                          null=True, blank=True,
                                          )
    LOW = "LL"
    MEDIUM = "ML"
    HIGH = "HL"

    LEVELS_OF_KNOWLEDGE_CHOICES = (
        (LOW, "Baixo"),
        (MEDIUM, "Médio"),
        (HIGH, "Alto"),
    )

    level_of_english = models.CharField(max_length=3,
                                        choices=LEVELS_OF_KNOWLEDGE_CHOICES,
                                        null=True, blank=True,
                                        )
    level_of_literature = models.CharField(max_length=3,
                                           choices=LEVELS_OF_KNOWLEDGE_CHOICES,
                                           null=True, blank=True,
                                           )
    level_of_history = models.CharField(max_length=3,
                                        choices=LEVELS_OF_KNOWLEDGE_CHOICES,
                                        null=True, blank=True,
                                        )
    level_of_biology = models.CharField(max_length=3,
                                        choices=LEVELS_OF_KNOWLEDGE_CHOICES,
                                        null=True, blank=True,
                                        )
    level_of_physics = models.CharField(max_length=3,
                                        choices=LEVELS_OF_KNOWLEDGE_CHOICES,
                                        null=True, blank=True,
                                        )
    level_of_math = models.CharField(max_length=3,
                                     choices=LEVELS_OF_KNOWLEDGE_CHOICES,
                                     null=True, blank=True,
                                     )

    SHORT_TERM = "STL"
    LIFE_LONG = "LLL"

    LEARNING_GOAL_CHOICES = (
        (SHORT_TERM, "Aprendizagem a curto prazo"),
        (LIFE_LONG, "Aprendizagem vitalícia"),
    )

    learning_goal = models.CharField(max_length=3,
                                     choices=LEARNING_GOAL_CHOICES,
                                     help_text="""'Aprendizagem a curto prazo' = aprender sobre um tópico específico;
                                               'Aprendizagem vitalícia' = aprender mais sobre uma matéria;""",
                                     null=True, blank=True,
                                     )

    #Felder and solomon
    #Sequential learners tend to gain understanding in linear steps, with each step following
    # logically from the previous one. Global learners tend to learn in large jumps, absorbing
    # material almost randomly without seeing connections, and then suddenly "getting it."

    SEQUENTIAL = "SQN"
    GLOBAL = "GLB"

    LEARNING_STYLE_CHOICES = (
        (SEQUENTIAL, "Aprendizagem sequencial"),
        (GLOBAL, "Aprendizagem global"),
    )

    learning_style = models.CharField(max_length=3,
                                      choices=LEARNING_STYLE_CHOICES,
                                      help_text=""""Aprendizagem sequencial = aprende linearmente (ex. lê um livro na sequência capítulo 1,2,3...)
                                                    Aprendizagem global = aprende pulando conteúdo (ex. lê o livro em ordem randômica cap. 1,5,3,9...)""",
                                      null=True, blank=True,
                                      )
    def __str__(self):
        return 'User %s - Learner %s' % (self.user_fk_id, self.pk)


class Movie(models.Model):
    movie_name = models.CharField(max_length=200)
    movie_description = models.TextField(max_length=2000)
    rationale = models.TextField(max_length=2000, null=True, blank=True)
    benefits = models.TextField(max_length=2000, null=True, blank=True)
    problems = models.TextField(max_length=2000, null=True, blank=True)
    objectives = models.TextField(max_length=2000, null=True, blank=True)
    movie_pic = models.ImageField(upload_to='pics/', null=True, blank=True)

    ENGLISH = "EN"
    LITERATURE = "LT"
    HISTORY = "HT"
    BIOLOGY = "BL"
    PHYSICS = "PH"
    MATH = "MT"

    KNOWLEDGE_AREA_CHOICES = (
        (ENGLISH, "Inglês"),
        (LITERATURE, "Literatura"),
        (HISTORY, "História"),
        (BIOLOGY, "Biologia"),
        (PHYSICS, "Física"),
        (MATH, "Matémática"),
    )
    movie_knowledge_area = models.CharField(max_length=2,
                                            choices=KNOWLEDGE_AREA_CHOICES, null=True, blank=True)
    movie_recommended_age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '%s - %s' % (self.id, self.movie_name)


class Rating(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True, blank=True)
    predicted_rating = models.DecimalField(max_digits=8, decimal_places=6,null=True, blank=True)
    context_time = models.DateTimeField('Date Rated', auto_now_add=True, null=True, blank=True)
    long = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return 'Learner %s - Movie %s' % (self.learner_id, self.movie_id)
