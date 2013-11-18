#!/usr/bin/env python
"""tests for Web Results / Selenium integration."""

import os
import PIL
from reportlab.platypus import SimpleDocTemplate, Image
from selenium import webdriver
import StringIO
import tempfile
import time
import unittest

from src.WebTestResults import WebTestResults
from tests.local_config.config import TEST_REMOTE

IE = webdriver.DesiredCapabilities.INTERNETEXPLORER


class TestPlatypus(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        img = PIL.Image.new('RGBA', (600, 600), (255, 0, 0))
        imgtmp = tempfile.mkstemp(suffix=".png")
        self.imgfilename = os.path.join(self.tmpdir, imgtmp[1])
        self.imgfile = img.save(self.imgfilename)

    def test_save_pdf_image(self):
        doc = SimpleDocTemplate(os.path.join(self.tmpdir,
                                             tempfile.mkstemp()[1]))
        doc.build([Image(self.imgfilename)])

    def test_getting_ie_image_pdf(self):
        driver = webdriver.Remote(TEST_REMOTE, IE)
        driver.get('http://google.com')
        inputElement = driver.find_element_by_name('q')
        inputElement.send_keys('cheese!')
        inputElement.submit()
        time.sleep(10)
        x = StringIO.StringIO(driver.get_screenshot_as_png())
        x.seek(0)
        img = PIL.Image.open(x)
        img.save(self.imgfilename, dpi=(300, 300))
        browser_name = driver.name
        caps = str(driver.capabilities)
        descaps = str(driver.desired_capabilities)
        cds = caps + '\n\n\n' + descaps
        driver.quit()
        results = WebTestResults()
        results.add_test_section_header(browser_name, cds)
        results.add_img_from_file(self.imgfilename)
        results.write_to_file('test.pdf')

if __name__ == '__main__':
    unittest.main()
