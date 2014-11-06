"""
Twitch urls
"""
from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView
from twitch import views

urlpatterns = patterns('',
    url(r'^.+$', RedirectView.as_view(url='/twitch/')),
    url(r'^$', views.index, name='index'),
)
