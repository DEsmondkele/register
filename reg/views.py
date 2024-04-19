from django.contrib.auth import authenticate
from django.shortcuts import render, redirect

from .form import SignUpForm


def homepage(request):
    return render(request, 'reg/index.html')


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'reg/register.html', {'form': form})


def login(request):
    global username
    if request.method == 'POST':
        username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('dashboard')
    return render(request, 'reg/login.html')


def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'reg/dashboard.html')
    else:
        return redirect('login')



