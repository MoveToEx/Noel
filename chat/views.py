from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required

from .models import *

@login_required(login_url='user:login')
def index(request: HttpRequest):
    context = {
        "user": request.user
    }
    return render(request, 'chat/index.html', context)
