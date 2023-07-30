from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.deconstruct import deconstructible
import os

@deconstructible
class Rename(object):
    def __init__(self, path):
        self.path = path
    
    def __call__(self, inst, name):
        ext = name.split('.')[-1]
        filename = f"{inst.username}.{ext}"
        return os.path.join(self.path, filename)

class User(AbstractUser):
    nickname = models.CharField('Nickname', max_length=64)
    sign = models.CharField('Signature', max_length=128)
    description = models.TextField('Description', max_length=512)
    background_image = models.ImageField('Background image', upload_to=Rename('user_images/background'), blank=True, null=True)
    avatar = models.ImageField('Avatar', upload_to=Rename('user_images/avatar'), blank=True, null=True)
    title = models.CharField('Title', max_length=32, default='Untitled')
    title_style = models.CharField('Title style string', max_length=32, default='normal')


