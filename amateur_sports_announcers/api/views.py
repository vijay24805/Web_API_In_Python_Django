"""
API views
"""
from rest_framework import viewsets
from api.serializers import TwitchSerializer
from twitch.models import Favorites


class TwitchViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows favorites to be viewed only.
    """
    queryset = Favorites.objects.all()
    serializer_class = TwitchSerializer

