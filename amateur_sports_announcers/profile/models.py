"""
model class to store data objects
"""
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

import urllib2
import json as simplejson

#channellist = [ ]
#viewerslist = []
#gameslist = []

#favChannels_list = []
#favTeams_list = []


def get_featuredinfo():
    """
    retrieving top channels from Twitch TV
    """
    channellist = [ ]
    viewerslist = []
    gameslist = []

    url = 'https://api.twitch.tv/kraken/streams/featured?limit=25&offset=0&client_id=jqsd54ktgrxu0x05kh6w2lt4l3zkfck'
    jsoncontents = urllib2.urlopen(url)
    dictObj = simplejson.load(jsoncontents)
    returnli = []
    for streamnum in range(len(dictObj["featured"])):
        returnli.append( (streamnum, \
        dictObj["featured"][streamnum]["stream"]["channel"]["display_name"], \
        dictObj["featured"][streamnum]["stream"]["channel"]["status"], \
        dictObj["featured"][streamnum]["stream"]["viewers"], \
        dictObj["featured"][streamnum]["stream"]["channel"]["game"], \
        str(dictObj["featured"][streamnum]["stream"]["channel"]["url"]\
         ).replace("http://www.twitch.tv/", "")) )    

        for stream in returnli:
            i = 0
            for s in  stream:
                i += 1
                if i == 2:
                    channellist.append(s)
                elif i == 4:
                    viewerslist.append(s)
                elif i == 5:
                    gameslist.append(s)
                    i = 0

    favchannelslist = [(str(s), str(s)) for s in channellist]
    favteamslist = [(s, s) for s in gameslist]

    return favchannelslist, favteamslist


class UserProfile(models.Model):
    """
    #created basic user interest profile and need to change later to get
    the channels from ASA site
    """
    favchannelslist, favteamslist = get_featuredinfo()
    mainUser = models.ForeignKey(User)
    FavoriteChannel = models.CharField(max_length = 100, \
             choices = favchannelslist)
    FavoriteTeam = models.CharField(max_length = 100, choices = favteamslist)
    Comment  = models.TextField(max_length = 30000)


class ProfileForm(ModelForm):
    """
    create Profileform to act as model
    """
    class Meta:
        """
        Meta class
        """
        model = UserProfile
        exclude = ['mainUser']




