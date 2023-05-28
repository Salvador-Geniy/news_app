from django.shortcuts import render
from django.views import View


class MainView(View):
    def get(self, request):
        user = request.user
        return render(request, 'main.html', context={'user': user})
