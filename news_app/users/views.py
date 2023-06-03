from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.views import View

from users.forms import UserRegistrationForm


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    extra_context = {'password': {
        'write_only': True
    }
    }


class UserLogoutView(LogoutView):
    template_name = 'users/logout.html'


class UserRegistrationView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'users/registration.html', context={'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.cleaned_data['group'] = 'Readers'
            user = form.save()

            group = Group.objects.get(name='Readers')
            if group:
                group.user_set.add(user)

            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password1']

            user = authenticate(
                username=username,
                password=raw_password
            )
            login(request, user)
            return redirect('/')

