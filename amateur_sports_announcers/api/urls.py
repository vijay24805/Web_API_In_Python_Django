"""
API urls
"""
from django.conf.urls import patterns, include, url
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'favorites', views.TwitchViewSet)
#router.register(r'favorites', views.TwitchViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
