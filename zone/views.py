from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from datetime import datetime
import uuid

from .models import *

class HttpResponseImATeaPot(HttpResponse):
    status_code = 418


@login_required(login_url='user:login')
def index(request: HttpRequest):
    posts = Post.objects.order_by('-pinned', '-pub_time')
    if len(posts) > 30:
        posts = posts[:30]
    context = {
        "user": request.user,
        "posts": posts
    }
    return render(request, 'zone/index.html', context)


@login_required(login_url='user:login')
def detail(request: HttpRequest, post_id: uuid.UUID):
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post=post)
    context = {
        "user": request.user,
        "post": post,
        "comments": comments
    }
    return render(request, 'zone/detail.html', context)

@login_required(login_url='user:login')
def comment(request: HttpRequest, post_id: uuid.UUID):
    if request.method == 'GET':
        return HttpResponseImATeaPot()
    Comment.objects.create(**{
        'author': request.user,
        'pub_time': datetime.now(),
        'post': Post.objects.get(id=post_id),
        'content': request.POST['content']
    }).save()
    return redirect('zone:detail', post_id)

@login_required(login_url='user:login')
def new(request: HttpRequest):
    if request.method == 'GET':
        return HttpResponseImATeaPot()
    elif request.method == 'POST':
        post = Post.objects.create(author=request.user, pub_time=datetime.now())
        post.content = request.POST['content']
        post.image = request.FILES['image']
        buf = BytesIO()
        for chunk in request.FILES['image'].chunks():
            buf.write(chunk)
        thumb = Image.open(buf)
        fmt = thumb.format
        thumb.thumbnail((512, 512))
        buf = BytesIO()
        thumb.save(buf, fmt)
        post.thumbnail = ContentFile(buf.getvalue())
        post.save()
        return redirect('zone:index')

