from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView

from users.forms import UserLoginForm


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    extra_context = {'password': {
        'write_only': True
    }
    }


class UserLogoutView(LogoutView):
    template_name = 'users/logout.html'
