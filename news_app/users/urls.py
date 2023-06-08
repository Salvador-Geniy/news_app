from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import UserLoginView, UserRegistrationView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='articles'), name='logout'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
]