# Create your views here.
from django.shortcuts import render
from .models import User, Barber, Admin 
import json 

def base_view(request):
    return render(request, 'base.html')

def login_view(request):
    return render(request, 'login.html')

def singup_view(request):
    return render(request, 'singup.html')

def save_chas_view(request):
    return render(request, 'save_chas.html')

def chat_view(request):
    return render(request, 'chat.html')





