from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Movie(models.Model):
    name = models.CharField(max_length=60, primary_key=True)
    year = models.CharField(max_length=60)
    director = models.CharField(max_length=60)
    genre = models.CharField(max_length=60)
    image = models.CharField(max_length=60,default="none")

#Relation between users and movies, using django auth users
class MovieUser(models.Model):
    idMovieUser = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    username = models.ForeignKey(User,on_delete=models.CASCADE)

