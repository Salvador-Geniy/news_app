from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from articles.models import Article, Category
from articles.views import ArticleCreateView


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

    def test_main_page_exists_at_desired_location(self):
        response = self.client.get('/news/')
        self.assertEqual(response.status_code, 200)

    def test_main_page_uses_correct_template(self):
        url = reverse('articles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/article_list.html')

    def test_get_articles_list_and_categories_list(self):
        url = reverse('articles')
        response = self.client.get(url)
        articles = Article.objects.all().order_by('-created_at')
        categories_list = list(Category.objects.all())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['articles']), articles.count())
        self.assertQuerysetEqual(response.context['articles'], articles)
        self.assertEqual(list(response.context['categories']), categories_list)

    def test_get_article(self):
        url = reverse('article-detail', args=(self.article_1.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], self.article_1)


class AccountTestCase(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create(username='test user 1')
        self.user_2 = User.objects.create(username='test user 2')
        self.user_admin = User.objects.create(username='test admin', is_superuser=True)
        self.category_1 = Category.objects.create(name='test category 1')
        self.category_2 = Category.objects.create(name='test category 2')
        self.article_1 = Article.objects.create(author=self.user_1, title='test article 1',
                                                text='test text 1', category=self.category_1)
        self.article_2 = Article.objects.create(author=self.user_1, title='test article 2',
                                                text='test text 2', category=self.category_1)
        self.article_3 = Article.objects.create(author=self.user_2, title='test article 3',
                                                text='test text 3', category=self.category_2)

    def test_create_article(self):
        self.assertEqual(3, Article.objects.all().count())
        url = reverse('add-article')
        data = {
            'title': 'test article 4',
            'text': 'test text 4',
            'category': self.category_2.id
        }
        self.client.force_login(self.user_1)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Article.objects.all().count(), 4)
        self.assertEqual(Article.objects.last().author, self.user_1)

    def test_user_page_exist_at_desired_location(self):
        url = reverse('user-articles')
        self.client.force_login(self.user_1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_page_does_not_work_for_unregistered_user(self):
        url = reverse('user-articles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/news/?next=/news/list/')

    def test_user_page_uses_correct_template(self):
        url = reverse('user-articles')
        self.client.force_login(self.user_1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'articles/article_user_list.html')

    def test_create_article_not_login_user_redirect(self):
        url = reverse('add-article')
        response = self.client.post(url)
        self.assertRedirects(response, '/news/?next=/news/add/')

    def test_get_articles_list_created_by_user(self):
        url = reverse('user-articles')
        self.client.force_login(self.user_1)
        response = self.client.get(url)
        expected_data = Article.objects.filter(author=self.user_1.id).order_by('-created_at')

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['object_list'], expected_data)

    def test_update_page_exist_at_desired_location(self):
        url = reverse('article-update', args=(self.article_1.id,))
        self.client.force_login(self.user_1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_page_does_not_work_for_non_author_article(self):
        url = reverse('article-update', args=(self.article_1.id,))
        self.client.force_login(self.user_2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/news/')

    def test_update_page_work_for_non_author_article_but_admin(self):
        url = reverse('article-update', args=(self.article_3.id,))
        self.client.force_login(self.user_admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_page_exist_at_desired_location(self):
        url = reverse('article-delete', args=(self.article_1.id,))
        self.client.force_login(self.user_1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_page_does_not_work_for_non_author_article(self):
        url = reverse('article-delete', args=(self.article_3.id,))
        self.client.force_login(self.user_1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/news/')

    def test_delete_page_work_for_non_author_article_but_admin(self):
        url = reverse('article-delete', args=(self.article_3.id,))
        self.client.force_login(self.user_admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
