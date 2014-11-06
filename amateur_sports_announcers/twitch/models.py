"""
Twitch models
"""
from django.db import models
from django.contrib.auth.models import User

class Favorites(models.Model):
    """
    Twitch Favorites
    """
    user = models.OneToOneField(User)
    favoriteStreams = models.TextField()

