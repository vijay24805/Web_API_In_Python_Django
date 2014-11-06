"""Views for the Twitter app"""
from django.shortcuts import render
from twitter.twitterauth import TwitterAuth

# Create your views here.
def index(request):
    """Instantiate TwitterAuth and pass to template"""
    twitterauth = TwitterAuth()
    twitterauth.set_access_token()
    context = {'title': twitterauth.get_tweets('"leage of legends"'), }
    return render(request, 'twitter/index.html', context)
