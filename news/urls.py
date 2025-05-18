from django.urls import path
# Импортируем созданное нами представление
from .views import *


urlpatterns = [
    # path — означает путь.
    # В данном случае путь ко всем публикациям у нас останется пустым.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.
    path('news/', NewsList.as_view(), name='news_list'),

    # pk — это первичный ключ публикации, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
    path('news/<int:pk>', NewDetail.as_view()),

    path('news/search/', news_search, name='news_search'),
    path('news/create/', NewCreate.as_view(), name='news_create'),
    path('articles/create/', ArticleCreate.as_view(), name='articles_create'),

    path('news/<int:pk>/edit/', NewUpdate.as_view(), name='news_edit'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='articles_edit'),

    path('news/<int:pk>/delete/', NewDelete.as_view(), name='news_delete'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='articles_delete'),
]
