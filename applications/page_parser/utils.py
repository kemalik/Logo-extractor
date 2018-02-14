import logging

from django.conf import settings
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from applications.page_parser.exceptions import BrowserClientException, LogoExtractorException

logger = logging.getLogger(__file__)


class HtmlTag(object):
    def __init__(self, tag, is_image):
        self.is_image = is_image
        self.tag = tag


class BrowserClient(object):
    def __init__(self):
        try:
            self.browser = webdriver.Remote(
                command_executor=settings.SELENIUM_URL,
                desired_capabilities=DesiredCapabilities.CHROME
            )
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

    def get_images_in_page(self):
        self.browser.find_elements_by_xpath('//body//img')

    def get_image_containers(self):
        self.browser.find_elements_by_xpath('//body//*[not(script|style|img)]')

    def __del__(self):
        self.browser.quit()


class LogoExtractor(object):
    def __init__(self, url):
        self.url = url

    def get_site_logo(self):
        browser_client = BrowserClient()
        logging.debug('Browser client initialized')

        try:
            result = browser_client.get_url_source(self.url)
        except BrowserClientException as e:
            logging.error(e)
            raise LogoExtractorException

        return result
