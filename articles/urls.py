from django.urls import path
from .views import home_view, article_detail_view, add_comment_view

app_name = 'articles'

urlpatterns = [
    path('', home_view, name='home'),
    path('article/<int:article_id>/', article_detail_view, name='article_detail'),
    path('article/<int:article_id>/comment/', add_comment_view, name='add_comment'),
]
