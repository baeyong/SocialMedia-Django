from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

class Post(models.Model):
    date = models.DateTimeField()
    new_post = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    profile_picture = models.FileField(blank=True)
    bio = models.CharField(max_length=255, blank=True)
    following = models.ManyToManyField(User, related_name='followers')
    content_type = models.CharField(max_length=255, null=True)

class Comment(models.Model):
    text = models.CharField(blank=True, max_length=100)
    date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    

