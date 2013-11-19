from selenium import webdriver
import unittest
import tempfile
import datetime

from src.WebTestResults import WebTestResults


class TestWebTestResults(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.test_results = WebTestResults()

    def test_web_test_results_build_report(self):
        t = datetime.datetime.now()
        self.driver.get('http://google.com')
        print 'got site'
        fn = tempfile.mkstemp(suffix='.png')[1]
        self.driver.get_screenshot_as_file(fn)
        print 'got screenshot'
        t = str(datetime.datetime.now() - t)
        heading = "Firefox Google Test"
        ver = self.driver.capabilities['version']
        plat = self.driver.capabilities['platform']
        text = 'version: {}\nplatform: {}\nwait: {}\n'.format(ver, plat, t)
        print 'adding section'
        self.test_results.add_section(heading, text, fn)
        fn = tempfile.mkstemp(suffix='.pdf')[1]
        self.test_results.write_to_file(fn)
        print fn
        self.driver.quit()
