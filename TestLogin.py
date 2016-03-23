from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

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



# stand alone
if __name__ == '__main__':
    unittest.main()
            