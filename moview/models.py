from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Movie(models.Model):
	title = models.CharField(max_length=200)
	genre = ArrayField(models.CharField(max_length=200))
	director = ArrayField(models.CharField(max_length=200))
	rating = models.FloatField()
	year = models.IntegerField()
	poster = models.CharField(max_length=200, default = '')
	release_date = models.DateField(datetime.now())
	detail_poster = models.CharField(max_length=200, default = '')
	rate_cnt = models.IntegerField(default=0)
	duration = models.IntegerField(default=0)
	description = models.CharField(max_length=100000)

class Rate(models.Model):
	user = models.ForeignKey(User, unique=False)
	movie = models.ForeignKey(Movie, unique=False)
	rating = models.FloatField()

	class Meta:
		unique_together = ("user", "movie")

class UserMatrix(models.Model):
	user = models.ForeignKey(User, unique=True, db_index=True)
	vector = ArrayField(models.FloatField())


class MovieMatrix(models.Model):
	movie = models.ForeignKey(Movie, unique=True, db_index=True)
	vector = ArrayField(models.FloatField())
	context_feature = ArrayField(models.FloatField(default=0))