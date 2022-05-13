from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Role


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'role', )
    fieldsets = (
        ('General', {
            'fields': ('username', 'password', 'role', )
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email', )
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', )
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined', )
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2', 'role', )
        }),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )