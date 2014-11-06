"""
API serializer
"""
from rest_framework import serializers
from twitch.models import Favorites


class TwitchSerializer(serializers.ModelSerializer):
    """
    api class that sets up the returns    
    """
    favorites = serializers.SerializerMethodField('get_favorites')
    class Meta:
        """
        returns the user id and their favorites
        """
        model = Favorites
        fields = ('id', 'favorites')

    def get_favorites(self, obj):
        """
        get the twitch favorites of all the users
        """
        return obj.favoriteStreams.split(', ')[1:]
