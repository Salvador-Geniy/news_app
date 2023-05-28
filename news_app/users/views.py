from django.contrib.auth.views import LoginView, LogoutView


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    extra_context = {'password': {
        'write_only': True
    }
    }


class UserLogoutView(LogoutView):
    template_name = 'users/logout.html'
