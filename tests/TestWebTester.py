from selenium import webdriver
from tests.local_config.config import TEST_REMOTE, TEST_DOMAIN

import unittest
from src.WebTester import WebTester, WebTest

class TestWebTester(unittest.TestCase):

    def test_web_tester(self):
        IE = webdriver.DesiredCapabilities.INTERNETEXPLORER
        FF = webdriver.DesiredCapabilities.FIREFOX
        SA = webdriver.DesiredCapabilities.SAFARI
        CH = webdriver.DesiredCapabilities.CHROME
        site = TEST_DOMAIN
        lst = [WebTest('Internet Explorer', TEST_REMOTE, IE, [site]),
               WebTest('Firefox', TEST_REMOTE, FF, [site]),
               WebTest('Chrome', TEST_REMOTE, CH, [site]),
               WebTest('Safari', TEST_REMOTE, SA, [site])]
        tester = WebTester(lst, "test")
        tester.start()
