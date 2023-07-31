from django import template
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import stringfilter
from datetime import datetime
import markdown as md

from .models import *

register = template.Library()

@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=[
        'markdown.extensions.fenced_code'
    ])


@login_required(login_url='user:login')
def index(request: HttpRequest):
    posts = Post.objects.all().order_by('-pub_time')
    if len(posts) > 30:
        posts = posts[:30]
    context = {
        "user": request.user,
        "posts": posts
    }
    return render(request, 'blog/index.html', context)


@login_required(login_url='user:login')
def post(request: HttpRequest, post_id: int):
    post = Post.objects.get(id=post_id)
    context = {
        'user': request.user,
        'post': post
    }
    return render(request, 'blog/post.html', context)


@login_required(login_url='user:login')
def comment(request: HttpRequest, post_id: int):
    pass


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
