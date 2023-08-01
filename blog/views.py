from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime

from .models import *


class HttpResponseImATeaPot(HttpResponse):
    status_code = 418

@login_required(login_url='user:login')
def index(request: HttpRequest):
    posts = Post.objects.all().order_by('-pub_time')
    if len(posts) > 30:
        posts = posts[:30]
    for post in posts:
        post.comment_count = Comment.objects.filter(post=post).count()
    context = {
        "user": request.user,
        "posts": posts
    }
    return render(request, 'blog/index.html', context)


@login_required(login_url='user:login')
def post(request: HttpRequest, post_id: int):
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post=post)
    context = {
        'user': request.user,
        'post': post,
        'comments': comments
    }
    return render(request, 'blog/post.html', context)


@login_required(login_url='user:login')
def comment(request: HttpRequest, post_id: int):
    if request.method == 'GET':
        return HttpResponseImATeaPot()
    elif request.method == 'POST':
        Comment.objects.create(**{
            'author': request.user,
            'pub_time': datetime.now(),
            'post': Post.objects.get(id=post_id),
            'content': request.POST['content'],
            'reply': request.POST['reply']
        }).save()
        return redirect('blog:post', post_id)


@login_required(login_url='user:login')
def new(request: HttpRequest):
    if request.method == 'GET':
        context = {
            "user": request.user,
        }
        return render(request, 'blog/new.html', context)
    elif request.method == 'POST':
        Post.objects.create(**{
            'author': request.user,
            'pub_time': datetime.now(),
            'title': request.POST['title'],
            'content': request.POST['content']
        }).save()
        return redirect('blog:index')
