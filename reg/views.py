from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken

from .form import SignUpForm


@csrf_exempt
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    token = refresh.token
    return {
        'refresh': str(refresh),
        'access': str(token),
    }


def homepage(request):
    return render(request, 'reg/index.html')


@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'User created successfully.'})
    else:
        form = SignUpForm()
    return JsonResponse({'message': 'Registration unsuccessful.'})


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            tokens = get_tokens_for_user(user)
            return JsonResponse({'tokens': tokens})
    return JsonResponse({'error': 'Invalid credentials.'}, status=400)


@csrf_exempt
def dashboard(request):
    if request.method == 'GET':
        return JsonResponse({'message': 'Dashboard'})
