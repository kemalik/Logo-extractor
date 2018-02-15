import logging

from django.conf import settings
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from applications.page_parser.constants import XPATH_NOT_SCRIPT_STYLE_IMG, XPATH_ALL_IMAGES
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
                desired_capabilities=DesiredCapabilities.CHROME,
                keep_alive=True
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

    def get_elements_by_xpath(self, xpath):
        return self.browser.find_elements_by_xpath(xpath)

    def get_images_in_page(self):
        images_in_page = []
        images = self.get_elements_by_xpath(XPATH_ALL_IMAGES)
        for image in images:
            images_in_page.append(
                HtmlTag(tag=image, is_image=True)
            )

        return images_in_page

    def get_image_containers(self):
        image_containers_in_page = []
        elements = self.get_elements_by_xpath(XPATH_NOT_SCRIPT_STYLE_IMG)

        for element in elements:
            element_style = element.value_of_css_property('background-image')
            if element_style != 'none':
                image_containers_in_page.append(
                    HtmlTag(element, False)
                )
        return image_containers_in_page

    def get_potential_logos(self):
        elements = [self.get_images_in_page() + self.get_image_containers()]
        return elements

    def __del__(self):
        self.browser.quit()


class LogoExtractor(object):
    def __init__(self, url):
        self.url = url

    def get_site_logo(self):
        browser_client = BrowserClient()
        logging.debug('Browser client initialized')

        browser_client.open_url(self.url)
        browser_client.get_potential_logos()

        try:
            result = browser_client.get_url_source(self.url)
        except BrowserClientException as e:
            logging.error(e)
            raise LogoExtractorException

        return result
