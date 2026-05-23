from django.urls import path
from . import views

app_name = 'scholarships'

urlpatterns = [
    # student
    path('',               views.scholarship_list,   name='list'),
    path('<int:pk>/',      views.scholarship_detail, name='detail'),
    # admin
    path('manage/',           views.admin_scholarship_list, name='admin_list'),
    path('manage/create/',    views.scholarship_create,     name='create'),
    path('manage/<int:pk>/edit/',   views.scholarship_edit,   name='edit'),
    path('manage/<int:pk>/delete/', views.scholarship_delete, name='delete'),
]