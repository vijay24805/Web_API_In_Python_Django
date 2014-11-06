from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'asa.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'asa.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^twitch/', include('twitch.urls')),
    url(r'^info/', include('info.urls')),
    url(r'^api/', include('api.urls')),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    (r'^accounts/', include('allauth.urls')),
    url(r'^broadcast/', 'broadcast.views.index', name='broadcast'),
    url(r'^accounts/createProfile/', "profile.views.createprofile", name='createProfile'),
    url(r'^accounts/viewProfile/', "profile.views.viewprofile", name='viewProfile'),
    url(r'^accounts/editProfile/', "profile.views.editprofile", name='editProfile'),
    url(r'^accounts/manageAccount/', "profile.views.manageaccount", name='manageAccount'),
    #url(r'^captcha/', include('captcha.urls')),
    url(r'^hot/channels/', "hot.views.hotchannel", name='hotChannel'),
    url(r'^hot/chat/', "hot.views.chat", name='hotChat'),
    #url(r'^hot/threadPosts/', "hot.views.threadPosts", name='hotThreadPosts'),
    #url(r'^hot/threads/([a-z 0-9]+)/$', "hot.views.threads", name='hotThreads'),
    url(r'^hot/topChannels/', "hot.views.topchannels", name='topChannels'),
    url(r'^twitter/', 'twitter.views.index', name='twitter'),
    url(r'^youtube/', 'twitch.views.youtube', name='youtube'),
    url(r'^sentimentAnalysis/analysis/', "sentimentAnalysis.views.readandparse", name="Sentiment"),
)
