from blogapp.models import Article
from django.contrib.syndication.views import Feed
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.urls import reverse_lazy, reverse

class ArticlesListView(ListView):
    queryset = (
        Article.objects
        .filter(published_at__isnull=False)
        .order_by('-published_at')
    )

class ArticleDetailView(DetailView):
    model = Article

class LatestArticlesFeed(Feed):
    title = 'Blog articles (Latest)'
    description = 'Обновление измененение и добавление статей'
    link = reverse_lazy('blogapp:articles')

    def items(self):
        return Article.objects.order_by('-published_at')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item:Article):
        return item.body[:200]

    def item_link(self, item:Article):
        return reverse('blogapp:article', kwargs={'pk':item.pk})