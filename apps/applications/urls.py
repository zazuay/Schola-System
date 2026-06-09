from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    # student
    path('apply/<int:scholarship_pk>/',      views.apply_view,     name='apply'),
    path('<int:application_pk>/upload/',     views.upload_view,    name='upload'),
    path('status/',                          views.status_view,    name='status'),
    
    # NEW: Notifications URLs
    path('notifications/',                   views.notifications_view, name='notifications'),
    path('notifications/mark-read/',         views.mark_all_read_view, name='mark_all_read'),

    # admin
    path('admin/',                           views.applicant_list,      name='admin_list'),
    path('admin/<int:pk>/',                  views.applicant_detail,    name='admin_detail'),
    path('admin/<int:pk>/status/',           views.update_status_view,  name='update_status'),
]