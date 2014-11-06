"""
Twitch Admin
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from twitch.models import Favorites

# Define an inline admin descriptor for Favorites model
# which acts a bit like a singleton
class FavoritesInline(admin.StackedInline):
    """
    Class used for admin profile of users, in line
    """
    model = Favorites
    can_delete = False
    verbose_name_plural = 'favorites'

# Define a new User admin
class UserAdmin(UserAdmin):
    """
    Class used for admin profile of users
    """
    inlines = (FavoritesInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
