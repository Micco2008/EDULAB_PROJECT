from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

__all__ = ['admin', 'UserAdmin', 'User']


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_editable = ('is_staff',)
    readonly_fields = ('username', 'last_login', 'date_joined')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
