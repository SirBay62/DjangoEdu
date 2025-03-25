from django.urls import path

from .views import (
    ArticlesListView,
    ArticleDetailView,
)

app_name = 'blogapp'

urlpatterns = [
    path ( 'articles/', ArticlesListView.as_view (), name='articles' ),
    path ( 'article/<int:pk>/', ArticleDetailView.as_view (), name='article' ),
]
