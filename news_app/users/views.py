from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

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




    # def get(self, request):
    #     if self.user.is_authenticated:
    #         return redirect('articles')
    #     form = UserRegistrationForm()
    #     return render(request, 'users/registration.html', context={'form': form})
    #
    # def post(self, request):
    #     form = UserRegistrationForm(request.POST)
    #     if form.is_valid():
    #         form.cleaned_data['group'] = 'Readers'
    #         user = form.save()
    #
    #         group = Group.objects.get_or_create(name='Readers')
    #         if group:
    #             group.user_set.add(user)
    #
    #         username = form.cleaned_data['username']
    #         raw_password = form.cleaned_data['password1']
    #
    #         user = authenticate(
    #             username=username,
    #             password=raw_password
    #         )
    #         login(request, user)
    #         return redirect('/news')

