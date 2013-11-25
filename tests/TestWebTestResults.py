"""
Simple sanity test for WebTestResults.

@author raphael.luckom
@license GPL v2.0 or later

"""
from selenium import webdriver
import unittest
import tempfile
import datetime

from src.WebTestResults import WebTestResults
from tests.local_config.config import TEST_DOMAIN


class TestWebTestResults(unittest.TestCase):

    """Test class."""

    def setUp(self):
        """Set up the test."""
        self.driver = webdriver.Firefox()
        self.test_results = WebTestResults()

    def test_web_test_results_build_report(self):
        """run a simple report."""
        t = datetime.datetime.now()
        self.driver.get(TEST_DOMAIN)
        t = str(datetime.datetime.now() - t)
        fn = tempfile.mkstemp(suffix='.png')[1]
        self.driver.get_screenshot_as_file(fn)
        heading = "Firefox Google Test"
        ver = self.driver.capabilities['version']
        plat = self.driver.capabilities['platform']
        text = 'version: {}\nplatform: {}\nwait: {}\n'.format(ver, plat, t)
        self.test_results.add_section(heading, text, fn)
        fn = tempfile.mkstemp(suffix='.pdf')[1]
        self.test_results.write_to_file(fn)
        self.driver.quit()
