"""
URLs for edx_hutech_news.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.hutech_news_page, name='hutech_news'),
    path('fragment/', views.hutech_news_fragment, name='hutech_news_fragment'),
    path('api/news/', views.hutech_news_json, name='hutech_news_json'),
    path('article/<int:article_id>/', views.hutech_news_detail, name='hutech_news_detail'),
]