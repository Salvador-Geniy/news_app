from django.contrib import admin
from django.contrib.admin import ModelAdmin

from articles.models import Category, Article


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    pass
