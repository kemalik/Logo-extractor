from django.conf import settings

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from applications.page_parser.exceptions import BrowserClientException


class BrowserClient(object):
    def __init__(self):
        try:
            self.chrome = webdriver.Remote(
                command_executor=settings.SELENIUM_URL,
                desired_capabilities=DesiredCapabilities.CHROME)
        except Exception as e:
            raise BrowserClientException('Unable init webdriver {}'.format(e))

    def get_url_source(self, url):
        try:
            self.chrome.get(url=url)
        except Exception as e:
            raise BrowserClientException(
                'Unable to get page source, {exception}'.format(exception=e)
            )
        return self.chrome.page_source

    def __del__(self):
        self.chrome.quit()
