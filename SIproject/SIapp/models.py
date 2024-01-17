from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Users(models.Model):
    email = models.EmailField(default='')
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    liked_posts= ArrayField(models.CharField(max_length=100, default=[]))
    profilePicture = models.ImageField(upload_to="media", default='media\pfp.png')
    bio = models.CharField(max_length=100, default = "user has no bio")
    
    
class Posts(models.Model):
    post = models.CharField(max_length=200)
    user = models.CharField(max_length=50)
    date = models.CharField(max_length=50, default='26/12/25')
    likes = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(upload_to="media", default=False)
    
    
