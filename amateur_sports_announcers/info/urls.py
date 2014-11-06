from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView
from info import views

urlpatterns = patterns('',
    url(r'^.+$', RedirectView.as_view(url='/info/')),
    url(r'^$', views.index, name='index'),
)
