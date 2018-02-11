from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from applications.page_parser.exceptions import BrowserClientException


class BrowserClient(object):
    def __init__(self):
        try:
            self.chrome = webdriver.Remote(
                command_executor='http://localhost:4444/wd/hub',
                desired_capabilities=DesiredCapabilities.CHROME)
        except Exception as e:
            raise BrowserClientException(e)

    def get_page(self, url):
        self.chrome.get(url=url)
        return self.chrome.page_source

    def __del__(self):
        self.chrome.quit()
