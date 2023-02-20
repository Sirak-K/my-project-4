from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile


# Create your views here.

@login_required(login_url='signin')
def index(request):
    header_text = "Welcome to my website!"
    
    return render(request, 'index.html', {'header_text': header_text})

