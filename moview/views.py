from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from .models import Movie
from .models import Rate
from .models import MovieMatrix
from .models import UserMatrix
from django.db.models import Q
import random

import scipy.io
import numpy as np

import os
import json

CONST_YEAR = 2015

settings_dir = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))

time = 1.
epsilon_init = 1
context_dim = 5
lambda_ = 0.1
tau = 0.0125

mMatricesQ = MovieMatrix.objects.all()
mMatrices = []
for mat in mMatricesQ:
	mMatrices.append(mat.vector)



# Create your views here.
def index(request):
	# Load highest rated movies, recent releases, top rated in recent years, 
	# and recommanded into UI
	uid = request.session.get('id', None)
	name = request.session.get('name', None)
	
	highestRatedMovies = Movie.objects.order_by('rating').reverse()[0:10]

	recentReleases = Movie.objects.order_by('release_date').reverse()[0:10]

	favoritesFromPastYear = Movie.objects.filter(year=CONST_YEAR).order_by('rating').reverse()[0:10]

	recommandedMovies = []

	if (uid != None):
		recList = decide(uid)
		recommandedMovies = Movie.objects.filter(pk__in=recList)

	#TO DO: Get recommanded

	context = {
		'highestRatedMovies' : highestRatedMovies,
		'recentReleases' : recentReleases,
		'favoritesFromPastYear' : favoritesFromPastYear,
		'recommandedMovies' : recommandedMovies,
		'name' : name
	}

	return render(request, "moview/index.html", context)

def signupPage(request):
	uid = request.session.get('id', None)
	if uid != None:
		return redirect('moview.views.index')
	return render(request, "moview/signup.html", {})

def signup(request):
	email = request.POST['email']
	name = request.POST['name']
	password = request.POST['password']
	newId = User.objects.all().count() + 1
	if not (User.objects.filter(email = email).exists()):
		user = User(id=newId, username=name, email=email, password=password, first_name = name)
		user.save()
		request.session['name'] = name
		request.session['email'] = email
		request.session['id'] = user.id
		addUser(user.id)
		return redirect('moview.views.index')
	else:
		errorMessage = "Email has already been registered!"
		context = {
			'errorMessage' : errorMessage
		}
		return render(request, 'moview/signup.html', context)

def signinPage(request):
	uid = request.session.get('id', None)
	if uid != None:
		return redirect('moview.views.index')
	return render(request, "moview/signin.html", {})

def signin(request):
	email = request.POST['email']
	password = request.POST['password']
	user = authenticate(username=email, password=password)
	if user is not None:
		request.session['name'] = user.first_name
		request.session['email'] = email
		request.session['id'] = user.id
		return redirect('moview.views.index')
	else:
		errorMessage = "Email address or password not correct!"
		context = {
			'errorMessage' : errorMessage
		}
		return render(request, 'moview/signin.html', context)

def logout(request):
	del request.session['name']
	del request.session['email']
	del request.session['id']
	return redirect('moview.views.index')

def movieDetail(request, movie_id):
	movie = get_object_or_404(Movie, pk=movie_id)
	name = request.session.get('name', None)
	return render(request, 'moview/movie_detail.html', {'movie' : movie, 'name' : name})

def search(request):
	keyword = request.GET['keyword']
	try:
		movies = Movie.objects.filter(Q(title__iexact=keyword) | (Q(title__icontains=keyword) & ~Q(title__iexact=keyword)))
	except Movie.DoesNotExist:
		return render(request, 'moview/search_result.html', {'movies' : 'NO_MATCH'})

	name = request.session.get('name', None)
	display_cnt = 10 if 10 >= len(movies) else len(movies)
	return render(request, 'moview/search_result.html', {'movies' : movies[0:display_cnt], 'name' : name})

def rate(request):
	uid = request.session.get('id', None)
	if uid == None:
		return HttpResponse("Please sign in first!")
	mid = request.GET['mid']
	movie = Movie.objects.get(pk=mid)
	rating = request.GET['rate']
	try:
		rate = Rate.objects.get(user_id=uid, movie_id=mid)
		rate.rating=rating
		rate.save()
	except ObjectDoesNotExist:
		rate = Rate(user=User.objects.get(pk=uid), movie=movie, rating=rating)
		rate.save()
	updateParameters(600, int(mid), float(rating))
	return HttpResponse("Thanks for your rating!")

def updateParameters(uid, mid, reward):
	global time
	time += 1
	U, V = sgd(uid, mid, reward)
	return U, V

def sgd(uid, mid, reward):
	global context_dim
	global lambda_
	global tau
	mMatrix = MovieMatrix.objects.get(movie_id=mid)
	V = np.asarray(mMatrix.vector)
	U = np.asarray(UserMatrix.objects.get(user_id=uid).vector)
	context_feature = mMatrix.context_feature
	V[:context_dim] = context_feature[:context_dim]
	r_estimate = np.dot(U, V)
	U += 2 * tau * ((reward - r_estimate) * V - lambda_ * U)
	V += 2 * tau * ((reward - np.dot(U[:context_dim], V[:context_dim]) - r_estimate) * U - lambda_ * V)
	V[:context_dim] = context_feature[:context_dim]
	return U, V

def addUser(uid):
	vectorTemp = np.squeeze(np.asarray(np.random.rand(1, 25))).tolist()
	um = UserMatrix(user=User.objects.get(pk=uid), vector=vectorTemp)
	um.save()

def getEpsilon():
	global time
	global epsilon_init
	return min(1.0 * epsilon_init / time, 0)

def decide(uid):
	global mMatrices

	epsilon = getEpsilon()
	min_reward = float('inf')
	min_idx = None
	selected = set()
	rec_list = list()
	rand_choice = None

	U = np.asarray(UserMatrix.objects.get(user_id=uid).vector)

	movieCnt = Movie.objects.count()

	for mid in range(1, movieCnt + 1):
		V = np.asarray(mMatrices[mid-1])
		if len(rec_list) < 5:
			rec_list.append(mid)

		else:
			min_reward = float('inf')
			for i in range(len(rec_list)):
				Vtemp = np.asarray(mMatrices[rec_list[i]-1])
				r_estimate = np.dot(U, Vtemp)

				if r_estimate < min_reward:
					min_reward = r_estimate
					min_idx = i

			r_estimate = np.dot(U, V)
			if r_estimate > min_reward:
				rec_list[min_idx] = mid


	for mid in rec_list:
		selected.add(mid)
	for i in range(len(rec_list)):
		if random.random() <= epsilon:
			rand_choice = random.randint(1, movieCnt+1)
			while rand_choice in selected:
				rand_choice = random.randint(1, movieCnt+1)
			rec_list[i] = rand_choice

	return rec_list

def average(rating, rate_cnt):
	average = ((11 * 3) + (rating * rate_cnt)) / float(11 + rate_cnt)
	return average

