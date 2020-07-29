from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Converting strings in python to human readible text
# Passing through translation engine
from django.utils.translation import gettext as _
from core import models


class UserAdmin(BaseUserAdmin):

    ordering = ['id']
    list_display = ['email', 'name']
    # Define sections for fieldsets in our change and create page
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            # Permissions that control the user
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    # Django admin docs:
    # User admin takes an add field sets which defines
    # fields from the add page (create user page)
    # We will customize this field set to include email, password
    # so we can create user with minimal data
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),

    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Tag)
