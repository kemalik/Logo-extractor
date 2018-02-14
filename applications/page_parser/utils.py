from django.conf import settings

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from applications.page_parser.exceptions import BrowserClientException


class BrowserClient(object):
    def __init__(self):
        try:
            self.browser = webdriver.Remote(
                command_executor=settings.SELENIUM_URL,
                desired_capabilities=DesiredCapabilities.CHROME)
        except Exception as e:
            raise BrowserClientException('Unable init webdriver {}'.format(e))

    def open_url(self, url):
        try:
            self.browser.get(url=url)
        except Exception as e:
            raise BrowserClientException(
                'Unable to open url {url}, {exception}'.format(url=url, exception=e)
            )

    def get_url_source(self, url):
        self.open_url(url)

        return self.browser.page_source

    def __del__(self):
        self.browser.quit()
