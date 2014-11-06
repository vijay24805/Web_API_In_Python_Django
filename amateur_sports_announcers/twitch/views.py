"""
Twitch Application
"""
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import urllib2
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from twitch.models import Favorites
import json as simplejson
import re
from twitter.twitterauth import TwitterAuth
from youtube import YouTube

def index(request):
    """
    index view for twitch
    """
    featured_game = get_featured_game()
    twitterauth = TwitterAuth()
    twitterauth.set_access_token()
    tweets = twitterauth.get_tweets(featured_game)
    user = request.user
    if user.is_authenticated():
        username = user.username
        logged_in = True
        search_li = ""
        if request.method == 'GET' and 'error' in request.GET:
            get_error = request.GET['error']
            if get_error:
                return HttpResponseRedirect("/twitch/")

        top_stream_id, featured_li = get_featured_info()

        if request.method == 'GET' and 'search' in request.GET:
            search_q = request.GET['search']
            if not (search_q == ""):
                if re.match("^[A-Za-z0-9_ ]*$", search_q):
                    search_li = search_q
                    top_stream_id, featured_li = get_game_info(search_q)

        if request.method == 'GET' and 'sort' in request.GET:
            sort_str = request.GET['sort']
            featured_li = sort_list(featured_li, sort_str)
    
        if request.method == 'GET' and 'favorite' in request.GET:
            favorite_id = request.GET['favorite']
            addrem_to_user_favorites(favorite_id, username)

        if request.method == 'GET' and 'watch' in request.GET:
            tmp_id = request.GET['watch']
            if re.match("^[A-Za-z0-9_ ]*$", tmp_id):
                top_stream_id = request.GET['watch']
        context = { 'username': username, 
                'logged_in': logged_in, 
                'favLi': get_user_favorites(username), 
                'favLiLenBool': \
                  len(get_user_favorites(username)) >= 2, 
                'featuredLi': featured_li, 
                'searchLi': search_li, 
                'streamID': top_stream_id,
                'featuredGame': featured_game,
                'tweets': tweets, }
        return render(request, 'twitch/index.html', context)
    else:
        return redirect('/accounts/login')


def get_featured_info():
    """
    get the featured info from api
    """
    url = 'https://api.twitch.tv/kraken/streams/featured?'+\
        'limit=35&offset=0&client_id=jqsd54ktgrxu0x05kh6w2lt4l3zkfck'
    json_contents = urllib2.urlopen(url)
    dict_obj = simplejson.load(json_contents)
    return_li = []
    for stream_num in range(len(dict_obj["featured"])):
        return_li.append( (stream_num, \
          dict_obj["featured"][stream_num]["stream"]["channel"]["display_name"], \
          dict_obj["featured"][stream_num]["stream"]["channel"]["status"], \
          dict_obj["featured"][stream_num]["stream"]["viewers"], \
          dict_obj["featured"][stream_num]["stream"]["channel"]["game"], \
          str(dict_obj["featured"][stream_num]["stream"]["channel"]["url"]).replace("http://www.twitch.tv/", "")) )
    return str(return_li[0][5]), return_li

def get_featured_game():
    """return featured game being show"""
    url = 'https://api.twitch.tv/kraken/streams/featured?'+\
        'limit=35&offset=0&client_id=jqsd54ktgrxu0x05kh6w2lt4l3zkfck'
    json_contents = urllib2.urlopen(url)
    dict_obj = simplejson.load(json_contents)
    return dict_obj["featured"][0]["stream"]["channel"]["game"]

def sort_list(featured_li, sort_str):
    """
    sorts the list
    """
    #cap sensitive
    sort_li = ["1", "2", "3", "4"]
    if sort_str in sort_li:
        if sort_str == "3":
            featured_li.sort(key=lambda x: x[int(sort_str)], reverse=True)
        else: 
            featured_li.sort(key=lambda x: x[int(sort_str)] if x[int(sort_str)]\
               is None else x[int(sort_str)].lower())
    return featured_li

def get_game_info(search_q):
    """
    get the game info from api
    """
    url = 'https://api.twitch.tv/kraken/search/streams?q='+str(search_q).replace(" ", "%20")+\
        '&type=suggest&client_id=jqsd54ktgrxu0x05kh6w2lt4l3zkfck'
    json_contents = urllib2.urlopen(url)
    dict_obj = simplejson.load(json_contents)
    return_li = []
    for stream_num in range(len(dict_obj["streams"])):
        return_li.append( (stream_num, \
          dict_obj["streams"][stream_num]["channel"]["display_name"], \
          dict_obj["streams"][stream_num]["channel"]["status"], \
          dict_obj["streams"][stream_num]["viewers"], \
          dict_obj["streams"][stream_num]["channel"]["game"], \
          str(dict_obj["streams"][stream_num]["channel"]["url"]).replace("http://www.twitch.tv/", "")) )
    ret_url = ""
    if return_li:
        ret_url = str(return_li[0][5])
    return ret_url, return_li

def addrem_to_user_favorites(favorite_id, username):
    """
    add and or remove the user favorite channels
    """
    usr = User.objects.get(username=username)
    try:
        fav_li = usr.favorites.favoriteStreams.split(', ')
        if favorite_id not in fav_li:
            fav_li.append(favorite_id)
        else:
            fav_li.remove(favorite_id)
        usr.favorites.favoriteStreams = ", ".join(str(x) for x in fav_li)
        usr.favorites.save()
    except ObjectDoesNotExist:
        usr = User.objects.get(username=username)
        usr.favorites, created = Favorites.objects.get_or_create(user=usr, \
            favoriteStreams="@")
        addrem_to_user_favorites(favorite_id, username)

def get_user_favorites(username):
    """
    get the user favorite channels
    """
    fav_li = []
    try:
        usr = User.objects.get(username=username)
        fav_li = usr.favorites.favoriteStreams.split(', ')
    except ObjectDoesNotExist:
        pass
    return fav_li

def youtube(request):
    """get the youtube page with popular games"""
    logged_in = False
    user = request.user
    if user.is_authenticated():
        logged_in = True
    youtube = YouTube()
    popular_games = youtube.get_popular_games()
    context = {'popular_games': popular_games,
                'logged_in': logged_in,  }
    return render(request, 'youtube/index.html', context)
