# -*- coding: utf-8 -*-
"""
Twitch Tests
"""
from django.test import TestCase
import twitch.views, re
from youtube import YouTube

class TestYoutube(TestCase):
    """Test class for Youtube.py"""
    def test_popular_games_instance(self):
        """Test if instantiated obj is YouTube obj"""
        youtube = YouTube()
        self.assertIsInstance(youtube, YouTube)
    def test_get_popular_games(self):
        """test if YouTube app can get popular games"""
        youtube = YouTube()
        self.assertIsNotNone(youtube.get_popular_games())
    def test_get_request_url_popular_games(self):
        """test if requeset url is set"""
        youtube = YouTube()
        self.assertIsNotNone(youtube.get_request_url_popular_games())
class TwitchMethodTests(TestCase):
    """
    _it is normal for these functions to fail if the api is not working or overloaded with requests from other people, try again later.
    """

    def test_get_featured_info(self):
        """
        should return a json reponse instead of crashing, where the first return is the top_stream_id
        the second return is a list of filtered J_sO_n response that we are interested in, 
        all streams should have at least 1 viewer otherwise test fail since it malfunctioned
        """
        top_stream_id, featured_li = twitch.views.get_featured_info()
        self.assertNotEqual(top_stream_id, "")
        #user should have an _iD
        for stream_num in range(len(featured_li)):
            self.assertNotEqual(int(featured_li[stream_num][3]), 0)
        
    def test_sort_list(self):
        """
        sorts the featured_li from lowest to highest or for viewers highest to lowest, we will only check the viewer order
        since the function is the same except reversed, done: if sort_str is out of range then it will not change the list
        edit: had to lower() to ignore cases when sorting
        """
        top_stream_id, featured_li = twitch.views.get_featured_info()
        ret_feature_li = twitch.views.sort_list(featured_li, "3")
        base_streamer = ret_feature_li[0][3]
        for i in range(len(ret_feature_li)):
            bool_statement = base_streamer >= ret_feature_li[i][3]
            self.assertEqual(bool_statement, True)
            base_streamer = ret_feature_li[i][3]
        ret_feature_li = twitch.views.sort_list(featured_li, "1") 
        #test id in order
        base_streamer_name = ret_feature_li[0][1]
        for i in range(len(ret_feature_li)):
            bool_statement = base_streamer_name.lower() <= \
              ret_feature_li[i][1].lower()
            self.assertEqual(bool_statement, True)
            base_streamer_name = ret_feature_li[i][1]

    def test_get_game_info(self):
        """
        if you enter a bad string fn should return null response instead of crashing, otherwise good data
        """
        top_stream_id, featured_li = twitch.views.get_game_info("adwkjaabd \
          dakwwjdas dasxwd") #bad input, assuming no one used this
        self.assertEqual(top_stream_id, "")
        self.assertEqual(featured_li, [])
        top_stream_id, featured_li = twitch.views.get_game_info("league") 
        #should be good input as long as there is one stream
        self.assertNotEqual(featured_li, []) 
        #this indicates that there is good data stored
        top_stream_id = ""
        featured_li = []
        search_q = u'神魔' #foreign input
        if not (search_q == ""):
            if re.match("^[A-Za-z0-9_ ]*$", search_q): #should be blocked here
                top_stream_id, featured_li = twitch.views.\
                  get_game_info(search_q) 
                #if passed this function should crash
        self.assertEqual(top_stream_id, "")
        self.assertEqual(featured_li, [])






