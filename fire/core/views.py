# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import User
import json 
from bs4 import BeautifulSoup #html v python X
from django.contrib.auth.decorators import login_required

soup = BeautifulSoup('save_chas.html', 'html.parser') #tyrsene v html

def base_view(request):
    return render(request, 'base.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            if '@' in username and '.' in username:
                user.role = 'barber'
            elif username == 'Admin':
                user.role = 'admin'
            else:
                user.role = 'user'
                
            user.save()
            return redirect('home_view')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'}, status=401)
    else:
        return render(request, 'login.html')

def singup_view(request):
    if request.method =='POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        if len(firstname) > 50 or len(lastname) > 50 or len(username) > 50:
            return render(request, 'singup.html', {'error': 'Firstname, lastname, and username must be 50 characters or less'}, status=401)
        if len(password) < 6 or len(password1) < 6:
            return render(request, 'singup.html', {'error': 'Password must be at least 6 characters long'}, status=401)
        if '@' in username:
            return render(request, 'singup.html', {'error': 'Username cannot contain @'}, status=401)
        if password == password1:
            if not User.objects.filter(username=username).exists():
                user = User(firstname=firstname, lastname=lastname, username=username, saved=None)
                user.set_password(password) 
                user.save()
                return redirect('home_view')
            else:
                return render(request, 'singup.html', {'error': 'Username already exists'}, status=401)
        else:
            return render(request, 'singup.html', {'error': 'Passwords do not match'}, status=401)
        
    else:
        return render(request, 'singup.html')

def save_chas_view(request):
    phone = request.POST.get('phone')
    date = request.POST.get('date')
    time = request.POST.get('time')
    if request.user.is_authenticated:
        target = soup.find(id = 'firstname')
        target.decompose() #iztrivane na elementa
        target = soup.find(id = 'lastname')
        target.decompose()
        firstname = request.user.firstname
        lastname = request.user.lastname
    else:
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        
    
    return render(request, 'save_chas.html')

def home_view(request):
    return render(request, 'home.html')

@login_required
def chat_view(request):
    return render(request, 'chat.html')







