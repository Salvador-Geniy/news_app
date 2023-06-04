from django.urls import path

from articles.views import ArticleListView, ArticleDetailView, \
    ArticleCreateView, ArticleUpdateView, ArticleDeleteView, CategoryDetailView

urlpatterns = [
    path('', ArticleListView.as_view(), name='articles'),
    path('article-detail/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('add/', ArticleCreateView.as_view(), name='add-article'),
    path('article-update/<int:pk>', ArticleUpdateView.as_view(), name='article-update'),
    path('article-delete/<int:pk>', ArticleDeleteView.as_view(), name='article-delete'),
    path('category-detail/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

]