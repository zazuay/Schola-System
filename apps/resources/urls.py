from django.urls import path
from . import views

app_name = 'resources'

urlpatterns = [
    path('', views.resources_view, name='list'),
    path('library/', views.category_list_view, name='category_list'),
    path('article/', views.article_detail_view, name='article_detail'),
    path('article/<int:pk>/', views.article_detail_view, name='article_detail'),
    path('templates/<int:pk>/download/', views.download_template_view, name='download_template'),
]
