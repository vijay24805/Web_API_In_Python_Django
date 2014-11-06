"""this file will allow us to connect to Twitter search api"""
import urllib, urllib2
import base64
import json

class TwitterAuth(object):
    """does Twitter authentication for us"""
    consumer_key = 'dT3bmSdTAeljNwYHq7f9URR7A'
    consumer_secret = 'fPHfFbNlUh87li4oDQ5DAkSfXae5B4CY8CK7YWZ7VEDFLiPEXa'
    consumer_key = urllib.urlencode({consumer_key:''})[:-1]
    consumer_secret = urllib.urlencode({consumer_secret:''})[:-1]
    def __init__(self):
        """init for the class"""
        self.tweets = []
        self.access_token = ''
        self.auth_string = TwitterAuth.consumer_key + \
                            ":" + TwitterAuth.consumer_secret
    def set_access_token(self):
        """get an access token with consumer_key and consumer_secret"""
        b64auth = base64.b64encode(self.auth_string)
        content_type = 'application/x-www-form-urlencoded;charset=UTF-8'

        headers = {
            'Authorization': 'Basic ' + b64auth,
            'Content-Type': content_type
        }
        data = {'grant_type':'client_credentials'}
        data = urllib.urlencode(data)
        req = urllib2.Request('https://api.twitter.com/oauth2/token',
                              data,
                              headers)
        response = urllib2.urlopen(req)
        the_page = response.read()
        json_obj = json.loads(the_page)
        self.access_token = json_obj['access_token']
    def get_auth_token(self):
        '''returns the current access/auth token'''
        return self.access_token
    def get_tweets(self, keyword):
        '''make simple request to twitter to search some tweets'''
        encoded_keyword = urllib.urlencode({keyword:''})[:-1]
        request_url = 'https://api.twitter.com/1.1/search/tweets.json?q=' +\
                       encoded_keyword
        headers = {
            'Authorization': 'Bearer ' + self.access_token
        }

        req = urllib2.Request(request_url, None, headers)
        response = urllib2.urlopen(req)
        the_page = response.read()

        json_obj = json.loads(the_page)
        statuses = json_obj['statuses']
        for status in statuses:
            user_tweet = '<a href="http://twitter.com/' + \
                    status['user']['screen_name'] + '">' + \
                    status['user']['screen_name'] + '</a>' + \
                     " said " + status['text']
            self.tweets.append(user_tweet)
        return self.tweets
