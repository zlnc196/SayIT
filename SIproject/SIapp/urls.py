from django.urls import path
from . import views

urlpatterns = [
    path('', views.intro, name='intro'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('confirm', views.confirm, name='confirm'),
    path('homepage', views.homepage, name='confirm'),
    path('profile', views.profile, name='profile'),
    path('dprofile', views.dprofile, name='dprofile'),
    path('AllPosts', views.AllPosts, name='AllPosts'),
    path('likedPosts', views.LikedPosts, name='likedPosts')
    ]