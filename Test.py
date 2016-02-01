from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

import time
import unittest
from ParallelTest import ParallelTest


class ParallelTests(ParallelTest):
    
    def setUp(self):
        ParallelTest.setUp(self)
    
    #
    #    This test simply attempts to login
    #
    def test1_login(self):
        try:
            element = WebDriverWait(self.driver, 20).until(EC.title_contains("Parallel.Works Account Owner"))
        except Exception, e:
            self.fail("Cannot login ")


    
    #
    #    This one runs an Openfoam analysis
    #
    def test2_findTools(self):
        try:
            element = WebDriverWait(self.driver, 20).until(EC.frame_to_be_available_and_switch_to_it("contentIframe"))
        except Exception, e:
            print "Caght exceptiuon", e
                
        
        self.driver.switch_to_frame("galaxyframePanel")

        #openfoam = self.driver.find_element_by_id('56290277e794f5b9410cd068_img')
        openfoam = self.driver.find_element_by_id('568b1b2a9cabc66638552e8a_img')
        self.assertNotEquals(openfoam, None, "Cannot find Openfoam button")
        openfoam.click()
        
        try:
            element = WebDriverWait(self.driver, 20).until(EC.frame_to_be_available_and_switch_to_it("galaxy_main"))
        except Exception, e:
            print "Caght exceptiuon", e
            
        time.sleep(5)
            
        #try:
        #    element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(By.ID, "execute"))
        #except Exception, e:
        #    print "Caght exceptiuon", e
        
        button = self.findElementByTagID("button", "execute")
        #self.assertNotEquals(button, None, "Cannot find Execute button")
        button.click()
        
        time.sleep(20)
        
        # Poll the progress bar looking for 100%
        #  wait for 10 minutes
        for dt in range(1,600):
            progress = self.getProgress()
            if "100%" in progress:
                break
            time.sleep(1)
            
        print "Openfoam Took ", dt, "Seconds"
        
        


# stand alone
if __name__ == '__main__':
    unittest.main()
            
