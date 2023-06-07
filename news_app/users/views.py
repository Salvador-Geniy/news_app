from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView

from users.forms import UserRegistrationForm


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('articles')


class UserRegistrationView(FormView):
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('articles')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(UserRegistrationView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/news/')
        return super(UserRegistrationView, self).get(*args, **kwargs)


class UserAccountView(DetailView):
    model = User
    # queryset = User.objects.all().prefetch_related('my_articles')
    context_object_name = 'user'
    template_name = 'users/user-detail.html'

    def get_queryset(self, *args, **kwargs):
        queryset = User.objects.filter(id=self.kwargs['pk']).prefetch_related('my_articles').all()
        return queryset


