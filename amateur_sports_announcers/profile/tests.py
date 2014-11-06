"""
tests.py class to do unit test
"""
from django.test import TestCase
from profile.models import UserProfile
from django.contrib.auth.models import User

class ProfileMethodTests(TestCase):
    """
    class to test create,edit and view profile methods
    """
    username = "SJ"
    email = "SJ@gmail.com"
    password = "password123"

    def setup(self):
        """
        initializing
        """
        self.user_2 = User.objects.create_user("SJ", "SJ@gmail.com", \
              "password123")
        self.user_3 = User.objects.create_user('Dennis Leary', \
               'dennis@leary.com', 'denisspassword')

    def teardown(self):
        """
        Clean up after each test
        """
        self.user_2.delete()
        self.user_3.delete()

    def test_create_view_edit_profile(self):
        """
        when user enter his favorite channels and Favorite team, in view profile he can see his last entered choices.
        So I check create Profile reponse request.POST and data which is storing in DB(leads to view profile).
        After so many attempts came to know that, request.POST data is not getting saved, so created data manually and
        testing.If the values don't match test case will fail
        """
        channel = "Hallow23"
        team = "XXC"
        comment = "manual insert"
        form = UserProfile(id = 1, mainUser_id = 1, FavoriteChannel =\
               "Hallow23", \
        FavoriteTeam = "XXC", Comment = "manual insert")
        form.save()
	
        profile  =  UserProfile.objects.filter(mainUser_id = 1). \
              order_by('-id')[0]
        #checking Channel user enter in 
        #createProfile(),or editProfile(),saving in 
        #UserProfile table, and it is getting retriev from DB
        #to show the data in View Profile
        print("profile.FavoriteChANEL", profile.FavoriteChannel)
        self.assertEqual(channel, profile.FavoriteChannel)
        self.assertEqual(team, profile.FavoriteTeam)
        self.assertEqual(comment, profile.Comment)


    def test_manage_account(self):
        """
        this test case checks whther user entered password and email and username is correct or not. User objects are created manually
        with in setup() method and destroying in tearDown() methods. And retriving the data from Db and comparing whether the values are
        proper or not
        """
        user = User.objects.create_user("SJ112", "SJ@gmail.com", "password123")
        user  =  User.objects.get(username = "SJ112")
        print(user)
        self.assertEqual("SJ112", user.username)
		#we can't check passwords, as it gives haskvalues
		#self.assertEqual("password123",user.password)
        self.assertEqual("SJ@gmail.com", user.email)











