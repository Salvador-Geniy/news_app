from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from articles.models import Article, Category


class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ArticleDetailView(DetailView):
    model = Article
    context_object_name = 'article'


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['title', 'text', 'category']
    success_url = reverse_lazy('articles')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ArticleCreateView, self).form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    fields = ['title', 'text']
    success_url = reverse_lazy('articles')


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    context_object_name = 'article'
    template_name_suffix = '_delete'
    success_url = reverse_lazy('articles')

