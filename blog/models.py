from django.db import models
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='blog_post', on_delete=models.CASCADE)
    title = models.CharField('Title', max_length=128)
    pub_time = models.DateTimeField('Published time')
    content = models.TextField('Content')

