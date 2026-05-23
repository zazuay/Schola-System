from django.contrib import admin
from .models import Scholarship

@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ['name', 'provider', 'deadline', 'country', 'level']
    search_fields = ['name', 'provider']