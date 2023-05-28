from django.contrib.auth.decorators import login_required
from django.urls import path

from articles.views import ArticleListView, ArticleDetailView

app_name = 'articles'

urlpatterns = [
    path('articles-list/', login_required(ArticleListView.as_view()), name='articles-all'),
    path('articles-list/<int:pk>/', ArticleDetailView.as_view(), name='articles-detail'),
]