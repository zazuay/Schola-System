from django.contrib import admin
from .models import (
    Application,
    Document,
    Notification
)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'scholarship', 'status', 'date_submitted']
    list_filter  = ['status']

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['application', 'type', 'uploaded_at']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'title',
        'type',
        'is_read',
        'created_at'
    ]

    list_filter = [
        'type',
        'is_read'
    ]

    search_fields = [
        'user__email',
        'title'
    ]