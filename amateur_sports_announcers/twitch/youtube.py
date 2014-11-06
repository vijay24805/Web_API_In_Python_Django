"""Helper functions for grabbing the keywords we need for YouTube page"""
import urllib2
import json

class YouTube(object):
    """class to try to connect to youtube"""
    def __init__(self):
        """init the empty list of videos"""
        self.popular_games = []
        self.request_url = 'https://api.twitch.tv/kraken/games/top'
    def get_request_url_popular_games(self):
        """get request url for twitch popular games"""
        return self.request_url
    def get_popular_games(self):
        """search twitter api for most popular game names"""
        req = urllib2.Request(self.get_request_url_popular_games())
        response = urllib2.urlopen(req)
        the_page = response.read()
        json_obj = json.loads(the_page)
        for item in json_obj['top']:
            self.popular_games.append(item['game']['name'])
        return self.popular_games
