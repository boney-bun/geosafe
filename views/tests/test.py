"""
Automated Test page using Selenium.
Testing scenario for meta search.

Requirements:
1. Geckodriver is a separate HTTP server (https://github.com/mozilla/geckodriver).
2. ChromeDriver (https://sites.google.com/a/chromium.org/chromedriver/getting-started) should be in /usr/local/bin on OSX.
3. Ie (can only run on windows, has not tested yet).

Notes:
1. We would need to redirect the code to local binary.
2. The code has not tested on any platform but OSX.
3. The test run under python's virtual environment
"""
import os
import platform

from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


# Selenium hasn't setup yet, connect to the staging server for testing instead.
# TODO revise the urls to localhost once it has deployed on docker.
test_server_url = "http://staging.geonode.kartoza.com/geosafe/metasearch"
test_meta_search_url = "http://staging.geonode.kartoza.com/geosafe/metasearch"  # url for meta_search.
test_id_csw_url = "Jakarta"
test_browser_title = "example.com"


class ListBrowser:
    def __init__(self):
        self._browsers = {}

    def set_browser(self, browser_name, browser_handler):
        self._browsers[browser_name] = browser_handler

    def get_browser(self, browser_name):
        return self._browsers[browser_name]

    def get_browsers(self):
        return self._browsers

    def firefox_browser(self):
        if platform.system() == "Darwin":
            self.path_to_firefox = "/Applications/Firefox.app/Contents/MacOS/firefox-bin"
            # fallback to homebrew installation for mac users
            if not os.path.exists(self.path_to_firefox):
                self.path_to_firefox = os.path.expanduser("~") + self.path_to_firefox
        elif platform.system() == "Windows":
            self.path_to_firefox = (self._find_exe_in_registry() or self._default_windows_location())
        # Lists all possible platforms for future use.
        # elif platform.system() == "Linux":
        #   self.start_cmd = "/path/to/Firefox/on/Linux"
        # elif platform.system() == 'Java' and os._name == 'nt':
        #    self.start_cmd = self._default_windows_location()

        self.binary = FirefoxBinary(self.path_to_firefox)

        try:
            browser = webdriver.Firefox(firefox_binary=self.binary)
            # self.browser = webdriver.Firefox()
            browser.get(test_server_url)
        except Exception as e:
            self.fail('Error getting server url from selenium tests\n%s' % e.message)

        self.set_browser("firefox", browser)

    def chrome_browser(self):
        self.set_browser("chrome", webdriver.Chrome)

    def IE_browser(self):
        self.set_browser("IE", webdriver.Ie)

    def get_handler(self, browserName):
        return self._browsers[browserName]

    def set_handler(self, browserHandler):
        self._browsers


# Initialise the unittest and everything else.
class TestFrontEnd(TestCase):
    """Run front end tests using selenium."""

#   path_to_firefox = ""
#   still didn't work properly
    submit_button = '//input[@type="submit"]'

    def setUp(self):
        self.browser = ListBrowser()
        self.browser.chrome_browser()
        self.browser.firefox_browser()
        self.browser.IE_browser()

    def test_view_firefox(self):
        browser = self.browser.get_browser("firefox")
        self.assertEqual(test_browser_title, browser.title)
        browser.find_element_by_name("csw_url").send_keys(test_id_csw_url)
        # None of the below three callings are working for parsing the submit button.
        #browser.find_elements_by_css_selector("btn btn-primary").click()
        #self.button_submit = browser.find_elements_by_xpath(self.submit_button)
        #self.button_submit.click()
        #self.browser.find_elements_by_id("submit").click()

        browser.quit()

    def test_view_chrome(self):
        browser = self.browser.get_browser("chrome")
        self.assertEqual(test_browser_title, browser.title)
        browser.find_element_by_name("csw_url").send_keys(test_id_csw_url)
        browser.quit()

    # IE can only run on Windows
    def test_view_ie(self):
        browser = self.browser.get_browser("IE")
        self.assertEqual(test_browser_title, browser.title)
        browser.find_element_by_name("csw_url").send_keys(test_id_csw_url)
        browser.quit()

    def tearDown(self):
        pass

'''
It is advised to run under python virtual environment.
Assume we are at the same folder with this file, type: python -m unittest test
'''
if __name__ == "__main__":
    unittest.main()

"""
Enable the two lines below when it has integrated to docker and geonode.
Command to execute: ./manage.py test

suite = unittest.TestLoader().loadTestsFromTestCase(TestFrontEnd)
unittest.TextTestRunner(verbosity=2).run(suite)
"""