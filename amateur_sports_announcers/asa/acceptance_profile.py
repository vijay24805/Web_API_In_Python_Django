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

    
    # test to check ASA login page exist or Not
    def test_create_profile(self):
        self.driver.get("http://sportsradio.herokuapp.com/accounts/login/")
        elem = self.driver.find_element_by_name("login")
        elem.send_keys("test")
        elem1 = self.driver.find_element_by_name("password")
        elem1.send_keys("testing")
        elem1.send_keys(Keys.RETURN)
        try:        
			self.assertEqual(self.driver.current_url, "http://sportsradio.herokuapp.com/")
        except AssertionError, e:
			raise Exception("Invalid User name or password- Might have to sign up first")
        #elem = self.driver.find_element_by_class_name("dropdown-menu")
        #td = elem.find_element_by_link_text('Manage Account')
        #tds = elem.find_element_by_tag_name('a')
        #tds.send_keys(Keys.RETURN)
        self.driver.get("http://sportsradio.herokuapp.com/accounts/createProfile/")
        


    # Remove this func if don't want firefox to exit
    def tearDown(self):
        self.driver.close()
    

if __name__ == "__main__":
    unittest.main()
