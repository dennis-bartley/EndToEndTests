from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

url = "http://eval.parallel.works/login/"

class ParallelTest(unittest.TestCase):
    
    def setUp(self):
        # Need to check the http return code here...
        self.driver = webdriver.Firefox()
        #self.driver = webdriver.Chrome()

        self.driver.implicitly_wait(20)
        self.driver.set_page_load_timeout(30)
        
        try:
            rc = self.driver.get(url)

        except Exception, e:
            print "Can't load: ", url
            self.driver.close()
            
        
        user = self.driver.find_element_by_name("username")
        user.send_keys("bartleyeval")
        
        password = self.driver.find_element_by_name("password")
        password.send_keys("bartley123")
        
        password.send_keys(Keys.RETURN)
        
    
    # 
    # Chrome seems to have difficulty sometimes finding elements by ID
    # This should work for Chrome as well as firefox
    #
    def findElementByTagID(self, tag, id):
        rc = None
        els = self.driver.find_elements_by_tag_name(tag)
        for el in els:
            if el.get_attribute("id"):
                rc = el
                break
        return rc
    
    def getProgress(self):
        rc = None
        progress = self.driver.find_element_by_class_name("progress-bar")
        return progress.text
        
    def tearDown(self):
        self.driver.quit()
 