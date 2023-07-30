from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
import django.contrib.auth as auth
from .models import *

@login_required(login_url='user:login')
def my(request: HttpRequest):
    context = {
        "user": request.user
    }
    return render(request, 'user/my.html', context)


@login_required(login_url='user:login')
def user(request: HttpRequest, user_id: int):
    target = User.objects.get(id=user_id)
    context = {
        "user": request.user,
        "target": target
    }
    return render(request, 'user/user.html', context)


@login_required(login_url='user:login')
def edit(request: HttpRequest):
    if request.method == 'GET':
        context = {
            "user": request.user
        }
        return render(request, 'user/edit.html', context)
    elif request.method == 'POST':
        user = request.user
        if request.POST['nickname']:
            user.nickname = request.POST['nickname']
        if request.POST['description']:
            user.description = request.POST['description']
        if request.POST['sign']:
            user.sign = request.POST['sign']
        if request.FILES.get('avatar'):
            user.avatar = request.FILES.get('avatar')
        if request.FILES.get('background_image'):
            user.background_image = request.FILES.get('background_image')
        user.save()
        return redirect('user:my')
    
def login(request: HttpRequest):
    if request.method == 'GET':
        return render(request, 'user/login.html')
    elif request.method == 'POST':
        user = auth.authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            auth.login(request, user)
            return redirect('zone:index')
        else:
            return redirect('user:login')
        

@login_required(login_url='user:login')
def logout(request: HttpRequest):
    if request.user:
        auth.logout(request)
    return redirect('user:login')

def register(request: HttpRequest):
    if request.method == 'GET':
        return render(request, 'user/register.html')
    elif request.method == 'POST':
        user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
        user.nickname = user.username
        user.save()
        return redirect('user:login')