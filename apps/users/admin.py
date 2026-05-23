from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'name', 'role', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Extra', {'fields': ('phone', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra', {'fields': ('name', 'phone', 'role')}),
    )
    ordering = ['email']