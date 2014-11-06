import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from random import randint
from settings import CAPTCHA_TEST_MODE

class AsaTestpage(unittest.TestCase):
    #setting up driver to Firefox
    def setUp(self):
        self.driver = webdriver.Firefox()

    db_UserID = "testBot000"
    db_UserPw = "uPW"+ db_UserID +"145s"

    
	# test to check ASA Home page exist or Not
    def test_homeASApage(self):
        self.driver.get("http://sportsradio.herokuapp.com/")				
        self.assertIn( "Amateur Sports Announcers",self.driver.title)
        elem = self.driver.find_element_by_id("b-menu-2")
        elem.send_keys("selenium")
        elem.send_keys(Keys.RETURN)		
        try:        
			self.assertEqual(self.driver.current_url, "http://sportsradio.herokuapp.com/")
        except AssertionError, e:
			raise Exception("This is not ASA homepage!!")


    
    # test to check ASA login page exist or Not
    def test_ulogin_ASApage(self):
        self.driver.get("http://sportsradio.herokuapp.com/accounts/login/")
        elem = self.driver.find_element_by_name("login")
        elem.send_keys("vijay")
        elem1 = self.driver.find_element_by_name("password")
        elem1.send_keys("password")
        elem1.send_keys(Keys.RETURN)
        try:        
			self.assertEqual(self.driver.current_url, "http://sportsradio.herokuapp.com/")
        except AssertionError, e:
			raise Exception("Invalid User name or password- Might have to sign up first")


       
    def test_signup_ASApage(self):
	#tests the sign up page, if captcha test mode is enabled you can see it create a new account
        self.driver.get("http://sportsradio.herokuapp.com/accounts/signup/")
        elem1 = self.driver.find_element_by_id("id_captcha_1")
        elem1.send_keys("PASSED") #need to set 'CAPTCHA_TEST_MODE = True' in settings.py
        elem1 = self.driver.find_element_by_id("id_first_name")
        elem1.send_keys("Kevin")
        elem1 = self.driver.find_element_by_id("id_last_name")
        elem1.send_keys("Durant")
	userID = "testBot"+str(randint(0,12345000)) #less chance of repeating id, if 'CAPTCHA_TEST_MODE = True'
        elem1 = self.driver.find_element_by_name("username")
        elem1.send_keys(userID)
        elem2 = self.driver.find_element_by_name("email")		
        elem2.send_keys(userID+"@testBot.com")
        elem3 = self.driver.find_element_by_name("password1")
        elem3.send_keys("uPW"+userID+"145s") #if account is created do not want random person to hack it
        elem4 = self.driver.find_element_by_name("password2")
        elem4.send_keys("uPW"+userID+"145s")
        elem4.send_keys(Keys.RETURN)
	if CAPTCHA_TEST_MODE:
		#if this mode is enabled, note that this must be reflected on the website as well
		self.assertEqual(self.driver.current_url, "http://sportsradio.herokuapp.com/")
		#needs to be the same, meaning captcha passed
	else:	
		self.assertEqual(self.driver.current_url, "http://sportsradio.herokuapp.com/accounts/signup/")
    
    
    
    # test if view stream page has a row of activeStreams
    def test_vactive_streams_exists(self):
                
        self.driver.get("http://sportsradio.herokuapp.com/")
        elem = self.driver.find_element_by_class_name("carousel-caption")
        tds=elem.find_element_by_link_text('Broadcast')
        #tds = elem.find_element_by_tag_name('a')
        tds.send_keys(Keys.RETURN)
        
           
        
    # test if view stream page has search
    def test_search_twitch(self):
        self.driver.get("http://sportsradio.herokuapp.com/accounts/login/")
        elem = self.driver.find_element_by_name("login")
        elem.send_keys("User")
        elem1 = self.driver.find_element_by_name("password")
        elem1.send_keys("userpass")
        elem1.send_keys(Keys.RETURN)
        elem2 = self.driver.find_element_by_link_text("Listen")
        elem2.click()
        elem3 = self.driver.find_element_by_id("searchtwitchinput")
        elem3.send_keys("diablo")
        elem4 = self.driver.find_element_by_id("searchtwitchbutton")
        elem4.send_keys(Keys.RETURN)
    
    
    # test if broadcast page exists
    def test_youtube_page(self):
        self.driver.get("http://sportsradio.herokuapp.com/")
        #elem = self.driver.find_element_by_class_name("carousel-caption")
        #tds=elem.find_element_by_link_text('Broadcast')
        #tds = elem.find_element_by_tag_name('a')
        tds = self.driver.find_element_by_id('youtube')       
        tds.send_keys(Keys.RETURN)
        try:        
			self.assertEqual(self.driver.current_url, "http://sportsradio.herokuapp.com/youtube/")
        except AssertionError, e:
			raise Exception("Youtube Link not available!!")
    
    
    def test_youtube_page(self):
        self.driver.get("http://sportsradio.herokuapp.com/")
        #elem = self.driver.find_element_by_class_name("carousel-caption")
        #tds=elem.find_element_by_link_text('Broadcast')
        #tds = elem.find_element_by_tag_name('a')
        tds = self.driver.find_element_by_id('youtube')       
        tds.send_keys(Keys.RETURN)
        try:        
			self.assertEqual(self.driver.current_url, "http://sportsradio.herokuapp.com/youtube/")
        except AssertionError, e:
			raise Exception("Youtube Link not available!!")
    
    def test_gameStreams(self):
	    #tests the sign up page, if captcha test mode is enabled you can see it create a new account
        self.driver.get("http://sportsradio.herokuapp.com/accounts/signup/")
        elem1 = self.driver.find_element_by_id("id_first_name")
        elem1.send_keys("Kevin")
        elem1 = self.driver.find_element_by_id("id_last_name")
        elem1.send_keys("Durant")
        userID = "testBot"+str(randint(0,12345000)) 
        #less chance of repeating id, if 'CAPTCHA_TEST_MODE = True'
        elem1 = self.driver.find_element_by_name("username")
        elem1.send_keys(userID)
        elem2 = self.driver.find_element_by_name("email")		
        elem2.send_keys(userID+"@testBot.com")
        elem3 = self.driver.find_element_by_name("password1")
        elem3.send_keys("uPW"+userID+"145s") #if account is created do not want random person to hack it
        elem4 = self.driver.find_element_by_name("password2")
        elem4.send_keys("uPW"+userID+"145s")
        elem4.send_keys(Keys.RETURN)
        tds = self.driver.find_element_by_id('twitch')       
        tds.send_keys(Keys.RETURN)
        try:        
			self.assertEqual(self.driver.current_url, "http://sportsradio.herokuapp.com/twitch/")
        except AssertionError, e:
			raise Exception("Games Link not available!!")
    
    	
    def test_tweets(self):
        self.driver.get("http://sportsradio.herokuapp.com/accounts/signup/")
        elem1 = self.driver.find_element_by_id("id_first_name")
        elem1.send_keys("Kevin")
        elem1 = self.driver.find_element_by_id("id_last_name")
        elem1.send_keys("Durant")
        userID = "testBot"+str(randint(0,12345000)) 
        #less chance of repeating id, if 'CAPTCHA_TEST_MODE = True'
        elem1 = self.driver.find_element_by_name("username")
        elem1.send_keys(userID)
        elem2 = self.driver.find_element_by_name("email")		
        elem2.send_keys(userID+"@testBot.com")
        elem3 = self.driver.find_element_by_name("password1")
        elem3.send_keys("uPW"+userID+"145s") #if account is created do not want random person to hack it
        elem4 = self.driver.find_element_by_name("password2")
        elem4.send_keys("uPW"+userID+"145s")
        elem4.send_keys(Keys.RETURN)
        tds = self.driver.find_element_by_id('twitch')       
        tds.send_keys(Keys.RETURN)
        self.driver.get("http://sportsradio.herokuapp.com/twitch")
        elem = self.driver.find_element_by_class_name("authenticated")
        tds = elem.find_element_by_tag_name('a')
        tds.send_keys(Keys.RETURN)
        try:        
			self.assertEqual(self.driver.current_url, "https://twitter.com/")
        except AssertionError, e:
			raise Exception("Twitter page not found")
    
 
    
    def test_selectChannel(self):
        self.driver.get("http://sportsradio.herokuapp.com/accounts/signup/")
        elem1 = self.driver.find_element_by_id("id_first_name")
        elem1.send_keys("Kevin")
        elem1 = self.driver.find_element_by_id("id_last_name")
        elem1.send_keys("Durant")
        userID = "testBot"+str(randint(0,12345000)) 
        #less chance of repeating id, if 'CAPTCHA_TEST_MODE = True'
        elem1 = self.driver.find_element_by_name("username")
        elem1.send_keys(userID)
        elem2 = self.driver.find_element_by_name("email")		
        elem2.send_keys(userID+"@testBot.com")
        elem3 = self.driver.find_element_by_name("password1")
        elem3.send_keys("uPW"+userID+"145s") #if account is created do not want random person to hack it
        elem4 = self.driver.find_element_by_name("password2")
        elem4.send_keys("uPW"+userID+"145s")
        elem4.send_keys(Keys.RETURN)
        tds = self.driver.find_element_by_id('twitch')       
        tds.send_keys(Keys.RETURN)
        self.driver.get("http://sportsradio.herokuapp.com/twitch")
        elem = self.driver.find_element_by_class_name("table")
        tds = elem.find_element_by_tag_name('a')
        tds.send_keys(Keys.RETURN)


    
    # Remove this func if don't want firefox to exit
    def tearDown(self):
        self.driver.close()
       

if __name__ == "__main__":
    unittest.main()
