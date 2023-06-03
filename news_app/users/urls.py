from django.urls import path

from users.views import UserLoginView, UserLogoutView, UserRegistrationView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
]