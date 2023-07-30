from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class UserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Profile',
            {
                'fields': (
                    'nickname',
                    'sign',
                    'description',
                    'background_image',
                    'avatar',
                    'title',
                    'title_style'
                ),
            },
        ),
    )


admin.site.register(User, UserAdmin)
