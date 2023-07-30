from django.db import models
from django.conf import settings
import os
from uuid import uuid4
from django.utils.deconstruct import deconstructible

@deconstructible
class Rename(object):
    def __init__(self, path):
        self.path = path

    def __call__(self, inst, name):
        ext = name.split('.')[-1]
        return f"{self.path}/{inst.id}.{ext}"

class Post(models.Model):
    id = models.UUIDField('UUID', primary_key=True, default=uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    content = models.CharField('Post Content', max_length=500)
    image = models.ImageField('Post image', upload_to=Rename('post_images'), blank=True, null=True)
    thumbnail = models.ImageField('Thumbnail', upload_to=Rename('post_thumbnail'), blank=True, null=True, editable=False)
    pub_time = models.DateTimeField('Published time')
    pinned = models.BooleanField('Pinned', default=False)

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    post = models.ForeignKey(Post, models.CASCADE)
    content = models.CharField('Comment content', max_length=500)
    pub_time = models.DateTimeField('Published time')
    reply = models.IntegerField('Reply index', default=-1)

