from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register', views.register, name="register"),
    path('login', views.user_login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
]

