from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'signin/', views.signinPage, name='signinPage'),
    url(r'signup/', views.signupPage, name='signupPage'),
    url(r'signupSubmit/', views.signup, name='signup'),
    url(r'signinSubmit/', views.signin, name='signin'),
    url(r'movie/(?P<movie_id>[0-9]+)/', views.movieDetail, name='movieDetail'),
    url(r'search/', views.search, name='search'),
    url(r'rate/', views.rate, name='rate'),
    url(r'logout/', views.logout, name='logout'),
]