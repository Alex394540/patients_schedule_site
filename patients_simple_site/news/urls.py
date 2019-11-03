from django.urls import path
from . import views

app_name = 'news'
urlpatterns = [
    path('news/<int:pk>/', views.read_item, name='read_item'),
    path('news/', views.show_news, name='show_news'),
]
