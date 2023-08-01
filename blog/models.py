from django.db import models
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='blog_post', on_delete=models.CASCADE)
    title = models.CharField('Title', max_length=128)
    pub_time = models.DateTimeField('Published time')
    content = models.TextField('Content')


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='blog_comment', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, models.CASCADE)
    content = models.CharField('Comment content', max_length=500)
    pub_time = models.DateTimeField('Published time')
    reply = models.IntegerField('Reply index', default=-1)
