from django.db import models
from time import strftime

# Create your models here.


class User(models.Model):
    user_first_name = models.CharField(max_length=100)
    user_last_name = models.CharField(max_length=200)
    user_email = models.EmailField(max_length=100)
    user_age = models.IntegerField()

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
                                        )
    level_of_literature = models.CharField(max_length=3,
                                           choices=LEVELS_OF_KNOWLEDGE_CHOICES,
                                           )
    level_of_history = models.CharField(max_length=3,
                                        choices=LEVELS_OF_KNOWLEDGE_CHOICES,
                                        )
    level_of_biology = models.CharField(max_length=3,
                                        choices=LEVELS_OF_KNOWLEDGE_CHOICES,
                                        )
    level_of_physics = models.CharField(max_length=3,
                                        choices=LEVELS_OF_KNOWLEDGE_CHOICES,
                                        )
    level_of_math = models.CharField(max_length=3,
                                     choices=LEVELS_OF_KNOWLEDGE_CHOICES,
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
                                      )
    def __str__(self):
        return self.user_first_name


class Movie(models.Model):
    movie_name = models.CharField(max_length=200)
    movie_description = models.TextField(max_length=1000)
    movie_pic = models.ImageField(upload_to='pics/')

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
                                            choices=KNOWLEDGE_AREA_CHOICES)
    movie_recommended_age = models.IntegerField()

    def __str__(self):
        return self.movie_name


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True, blank=True)
    predicted_rating = models.IntegerField(null=True, blank=True)
    context_time = models.DateTimeField('Date Rated', null=True, blank=True)
    long = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return 'User %s - Movie %s' % (self.user_id, self.movie_id)
