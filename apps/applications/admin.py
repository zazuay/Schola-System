from django.contrib import admin
from .models import Application, Document

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'scholarship', 'status', 'date_submitted']
    list_filter  = ['status']

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['application', 'type', 'uploaded_at']