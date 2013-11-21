"""
Creates a report showing listed resources under listed driver capabilities.

@author raphaelluckom@gmail.com
@license GPL v2.0 or later

"""
from collections import namedtuple
import datetime
from selenium import webdriver
import tempfile

from src.WebTestResults import WebTestResults

WebTest = namedtuple('WebTest', ['browser_name',
                                 'browser_node_uri',
                                 'browser_selenium_spec',
                                 'resources_to_test'])


class WebTester(object):

    """Visits pages in browsers, takes screenshots."""

    def __init__(self, tests, report_name):
        """constructor.

        @param tests (list) : WebTest namedtuples
        @param report_name (str) : name for the report. Used in filename.

        """
        self._tests = tests
        self._results = WebTestResults()
        self._report_name = report_name

    def start(self):
        """run the tests."""
        for test in self._tests:
            self.run_test(test)
        self._results.write_to_file(self._report_name)

    def run_test(self, test):
        """run test.

        @param test (WebTest) : webtest namedtuple

        """
        driver = webdriver.Remote(test.browser_node_uri,
                                  test.browser_selenium_spec)
        for resource in test.resources_to_test:
            t = datetime.datetime.now()
            driver.get(resource)
            fn = tempfile.mkstemp(suffix='.png')[1]
            driver.get_screenshot_as_file(fn)
            t = str(datetime.datetime.now() - t)
            heading = '{} Test'.format(resource)
            ver = driver.capabilities['version']
            plat = driver.capabilities['platform']
            text = 'Browser: {}\nVersion: {}\nPlatform: {}\nWait: {}\n'
            text = text.format(test.browser_name, ver, plat, t)
            self._results.add_section(heading, text, fn)
        driver.quit()
