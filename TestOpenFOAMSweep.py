from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from django.utils.encoding import smart_str, smart_unicode

import time
import unittest
from ParallelTest import ParallelTest


class ParallelTests(ParallelTest):
    
    def setUp(self):
        ParallelTest.setUp(self)
    
    #
    #    This one runs an Openfoam analysis
    #
    def test2_OpenFoamSweep(self):
        try:
            element = WebDriverWait(self.driver, 20).until(EC.frame_to_be_available_and_switch_to_it("contentIframe"))
        except Exception, e:
            print "Caght exceptiuon", e
                
        self.driver.switch_to_frame("galaxyframePanel")

        openfoam = None

        links = self.driver.find_elements_by_class_name("menuitem")

        for div in links:
            try:
                title = div.get_attribute("title")
                if ("openfoamsweep" in title):
                    openfoam=div
            except Exception, e:
                print "Exception", e

        openfoam.click()
        
        try:
            element = WebDriverWait(self.driver, 20).until(EC.frame_to_be_available_and_switch_to_it("galaxy_main"))
        except Exception, e:
            print "Caught exception", e
            
        time.sleep(10)
            
        try:
            openfoamCaseInput = self.driver.find_element_by_id("select2-chosen-2")
        except Exception, e:
            print "Can't fine Case Input field", e
            self.fail("No case input field")
            

        try:
            caseInputFile = self.driver.find_element_by_id("uid-5")
        except Exception, e:
            self.fail("Can't find UID-5")
            
        try:
            selectElement = caseInputFile.find_element_by_tag_name("select")
            selector = Select(selectElement)
            selector.select_by_visible_text("8: parametric_openfoam_inputs.tgz")
        except Exception, e:
            print e
            self.fail("can,t find the select list ")
            
        try:
            caseInputFile = self.driver.find_element_by_id("uid-7")
        except Exception, e:
            self.fail("Can't find UID-5")
            
        try:
            selectElement = caseInputFile.find_element_by_tag_name("select")
            selector = Select(selectElement)
            selector.select_by_visible_text("7: blockMeshDict.template")
        except Exception, e:
            print e
            self.fail("can,t find the select list ")
            
        try:
            caseInputFile = self.driver.find_element_by_id("uid-9")
        except Exception, e:
            self.fail("Can't find UID-9")
            
        try:
            selectElement = caseInputFile.find_element_by_tag_name("select")
            selector = Select(selectElement)
            selector.select_by_visible_text("5: parametric_40runs.sweep")
        except Exception, e:
            print e
            self.fail("can,t find the select list ")
            
        
        
        
        time.sleep(20)
        
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
        
        # Find out if there were any errors
        # The appSummary table has a row with a count of the number of failed runs
        #
        # Collect the data from the Summary table
        #
        summary = {}
        try:
            summaryTable = self.driver.find_element_by_id("appSummary")
        except: 
            self.fail("Cannot find appSummary table")
        try:
            rows = summaryTable.find_elements_by_tag_name("tr")
            
            for row in rows:
                columns = row.find_elements_by_tag_name("td") 
                summary[columns[0].text] = columns[1].text

        except Exception, e:
            print "Caught ", e
            self.fail(e)
            
        try:
            if summary["Active"] != "0":
                self.fail("Still have active processes: " + summary["Active"])
        except Exception, e:
            self.fail("Can't find an Active entry in the summary  table")
            
        try:
            if summary["Failed"] != "0":
                self.fail("Some processes failed: " + summary["Failed"])
        except Exception, e:
                self.fail("Can't find an Failed entry in the summary table")
                
# stand alone
if __name__ == '__main__':
    unittest.main()
            
