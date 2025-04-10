from django.db import models

class Vacancy(models.Model):
    text = models.CharField(max_length=2000)

class Movie(models.Model):
    movie_title = models.CharField(max_length=150)
    release_year = models.IntegerField()

    def __str__(self):
        return self.movie_title
