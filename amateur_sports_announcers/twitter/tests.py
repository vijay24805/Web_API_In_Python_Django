"""Tests for the Twitter module"""
from django.test import TestCase
from twitter.twitterauth import TwitterAuth

class TestTwitterAuth(TestCase):
    """Test class for Twitter Authorization and Twitter functions"""
    def test_instantiating_object(self):
        """Test instantiating TwitterAuth obj"""
        twitterauth = TwitterAuth()
        self.assertIsInstance(twitterauth, TwitterAuth)
    def test_self_tweets(self):
        """Test if self.tweet is alive after instantiation"""
        twitterauth = TwitterAuth()
        self.assertIsNotNone(twitterauth.tweets)
    def test_self_tweets_is_list(self):
        """Test if self.tweets is indeed a list obj"""
        twitterauth = TwitterAuth()
        self.assertIsInstance(twitterauth.tweets, list)
    def test_self_tweets_empty(self):
        """Test if self.tweets is empty at instantiation"""
        twitterauth = TwitterAuth()
        self.assertIs(len(twitterauth.tweets), 0)
    def test_self_access_token_set(self):
        """Test if access_token is empty when instantiated"""
        twitterauth = TwitterAuth()
        self.assertEqual(twitterauth.access_token, '')
    def test_set_access_token(self):
        """Test set_access_token()"""
        twitterauth = TwitterAuth()
        twitterauth.set_access_token()
        self.assertIsNotNone(twitterauth.access_token)
    def test_auth_token_not_none(self):
        """Test if auth_token generated and not None"""
        twitterauth = TwitterAuth()
        twitterauth.set_access_token()
        self.assertIsNotNone(twitterauth.get_auth_token())
    def test_tweets_in_array(self):
        """Test that there are tweets in the array"""
        twitterauth = TwitterAuth()
        twitterauth.set_access_token()
        self.assertNotEqual(len(twitterauth.get_tweets('starcraft')), 0)
