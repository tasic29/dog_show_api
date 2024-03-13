from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUerAdmin

from core.models import MyUser


@admin.register(MyUser)
class UserAdmin(BaseUerAdmin):
    list_display = ['id', 'username', 'email', 'first_name', 'last_name']
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "email", "first_name", "last_name"),
            },
        ),
    )
