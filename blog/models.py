from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.conf import settings
from datetime import date

import uuid



class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    

    def __str__(self):
        return self.username
    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.username)])

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)


    def __str__(self):
        return f'Profile of {self.user.username}'
    
    def get_absolute_url(self):
        return reverse('user-profile', args=[str(self.user.username)])



class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    tags = models.CharField(max_length=200, blank=True, null=True)



    

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post-detail', args=[str(self.id)])

    

# Create your models here.
class Comment (models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
    
