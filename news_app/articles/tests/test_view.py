from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from articles.models import Article, Category


class MainPageTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test user')
        self.category_1 = Category.objects.create(name='test category 1')
        self.category_2 = Category.objects.create(name='test category 2')
        self.article_1 = Article.objects.create(author=self.user, title='test article 1',
                                                text='test text 1', category=self.category_1)
        self.article_2 = Article.objects.create(author=self.user, title='test article 2',
                                                text='test text 2', category=self.category_1)
        self.article_3 = Article.objects.create(author=self.user, title='test article 3',
                                                text='test text 3', category=self.category_2)

    def test_get_articles_list_and_categories_list(self):
        url = reverse('articles')
        response = self.client.get(url)
        articles = Article.objects.all().order_by('-created_at')
        categories_list = list(Category.objects.all())

        self.assertEqual(200, response.status_code)
        self.assertEqual(len(response.context['articles']), articles.count())
        self.assertQuerysetEqual(response.context['articles'], articles)
        self.assertEqual(list(response.context['categories']), categories_list)

    def get_article(self):
        url = reverse('article-detail', args=(self.article_1.id,))
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.article_1, response.context['object'])
