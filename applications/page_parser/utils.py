import logging
import re

from django.conf import settings
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from applications.page_parser.constants import (
    XPATH_NOT_SCRIPT_STYLE_IMG, XPATH_ALL_IMAGES,
    REGEX_PATTERN_SUBSTRING_FROM_QUOTES, CSS_PROPERTY_BACKGROUND_IMAGE
)
from applications.page_parser.exceptions import BrowserClientException, LogoExtractorException

logger = logging.getLogger(__file__)


class HtmlTag(object):
    def __init__(self, tag, is_image=False):
        self.is_image = is_image
        self.tag = tag

    def _get_my_css_value(self, property_name):
        return self.tag.value_of_css_property(property_name)

    def _parse_url(self, text):
        found = re.findall(REGEX_PATTERN_SUBSTRING_FROM_QUOTES, text)
        if found:
            return found[0]
        return None

    def get_image_url(self):
        if self.is_image:
            return ''

        css_value = self._get_my_css_value(CSS_PROPERTY_BACKGROUND_IMAGE)

        return self._parse_url(css_value)


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
        images = self.get_elements_by_xpath(XPATH_ALL_IMAGES)

        images_in_page = [HtmlTag(tag=image, is_image=True) for image in images]

        return images_in_page

    def _has_tag_background_style(self, element):
        element_style = element.value_of_css_property(CSS_PROPERTY_BACKGROUND_IMAGE)
        return element_style != 'none'

    def get_image_containers(self):
        not_image_tags = self.get_elements_by_xpath(XPATH_NOT_SCRIPT_STYLE_IMG)

        elements_with_bg_style = filter(self._has_tag_background_style, not_image_tags)

        image_containers = [HtmlTag(tag=tag) for tag in elements_with_bg_style]

        return image_containers

    def get_potential_logos(self):
        return self.get_images_in_page() + self.get_image_containers()

    def __del__(self):
        self.browser.quit()


class LogoExtractor(object):
    def __init__(self, url):
        self.url = url

    def get_site_logo(self):
        browser_client = BrowserClient()
        logging.debug('Browser client initialized')

        browser_client.open_url(self.url)
        for i in browser_client.get_potential_logos():
            print(i.get_image_url())

        try:
            result = browser_client.get_url_source(self.url)
        except BrowserClientException as e:
            logging.error(e)
            raise LogoExtractorException

        return result
