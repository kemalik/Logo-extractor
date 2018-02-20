import logging
import re

from django.conf import settings
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from applications.page_parser.constants import (
    XPATH_ALL_IMAGES,
    REGEX_PATTERN_SUBSTRING_FROM_QUOTES, CSS_PROPERTY_BACKGROUND_IMAGE,
    CSS_PROPERTY_DISPLAY, CSS_PROPERTY_VISIBILITY, CSS_PROPERTY_VALUE_NONE, CSS_PROPERTY_VALUE_HIDDEN,
    SCRIPT_APPEND_CLASS_IMAGE_CONTAINERS)
from applications.page_parser.exceptions import BrowserClientException, LogoExtractorException

logger = logging.getLogger(__file__)


class HtmlTag(object):
    def __init__(self, tag, is_image=False):
        self.is_image = is_image
        self._tag = tag
        self._point = 1
        self._excluded = False

    def _get_my_css_value(self, property_name):
        return self._tag.value_of_css_property(property_name)

    def exclude(self):
        self._excluded = True

    def is_excluded(self):
        return self._excluded

    def get_point(self):
        if self._excluded:
            return 0
        return self._point

    def add_point(self, point):
        self._point += point

    def _parse_url(self, text):
        found = re.findall(REGEX_PATTERN_SUBSTRING_FROM_QUOTES, text)
        if found:
            return found[0]
        logging.warning('Style {} no have url'.format(text))
        return None

    def get_image_url(self):
        if self.is_image:
            return self._tag.get_attribute('src')

        css_value = self._get_my_css_value(CSS_PROPERTY_BACKGROUND_IMAGE)

        return self._parse_url(css_value)

    def is_visible(self):
        if self._get_my_css_value(CSS_PROPERTY_DISPLAY) == CSS_PROPERTY_VALUE_NONE:
            return False
        if self._get_my_css_value(CSS_PROPERTY_VISIBILITY) == CSS_PROPERTY_VALUE_HIDDEN:
            return False
        return True

    def get_size(self):
        return self._tag.size

    def get_coordinates(self) -> dict:
        return self._tag.location

    def get_parent_tag(self):
        parent_tag = self._tag.find_element_by_xpath('..')
        return HtmlTag(parent_tag)

    def get_name(self):
        return self._tag.tag_name

    def get_attribute_value(self, attribute):
        return self._tag.get_attribute(attribute)


class BrowserClient(object):
    def __init__(self, url):
        try:
            self.browser = webdriver.Remote(
                command_executor=settings.SELENIUM_URL,
                desired_capabilities=DesiredCapabilities.CHROME,
                keep_alive=True
            )
        except Exception as e:
            raise BrowserClientException('Unable init webdriver {}'.format(e))
        self.url = url
        self._open_url()

    def _open_url(self):
        try:
            self.browser.get(url=self.url)
        except Exception as e:
            raise BrowserClientException(
                'Unable to open url {url}, {exception}'.format(url=self.url, exception=e)
            )

    def get_url_source(self):
        return self.browser.page_source

    def get_elements_by_xpath(self, xpath):
        return self.browser.find_elements_by_xpath(xpath)

    def get_elements_by_class(self, class_name):
        return self.browser.find_elements_by_class_name(class_name)

    def get_images_in_page(self):
        images = self.get_elements_by_xpath(XPATH_ALL_IMAGES)

        images_in_page = [HtmlTag(tag=image, is_image=True) for image in images]

        return images_in_page

    def get_image_containers(self):
        self.browser.execute_script(SCRIPT_APPEND_CLASS_IMAGE_CONTAINERS)

        elements_with_bg_style = self.get_elements_by_class('bg_found')

        image_containers = [HtmlTag(tag=tag) for tag in elements_with_bg_style]

        return image_containers

    def get_potential_tags(self):
        return self.get_images_in_page() + self.get_image_containers()

    def __del__(self):
        self.browser.quit()


class LogoExtractor(object):
    def __init__(self, url):
        self.url = url

    def _give_points_for_tag(self, tag: HtmlTag) -> HtmlTag:
        from applications.page_parser.pipelines import point_pipeline
        for checker in point_pipeline:
            tag = checker(tag)
            if tag.is_excluded():
                break
        logging.info('Image url: {} pointed: {} '.format(tag.get_image_url(), tag.get_point()))
        return tag

    def _get_max_pointed_image(self, pointed_tags: list):
        return max(pointed_tags, key=lambda item: item.get_point())

    def _try_extract(self):

        try:
            browser_client = BrowserClient(self.url)
            logging.info('Browser client initialized')
            result = browser_client.get_potential_tags()
        except BrowserClientException as e:
            logging.error(e)
            raise LogoExtractorException(e)

        if result:
            pointed_tags = list(map(self._give_points_for_tag, result))

            tag = self._get_max_pointed_image(pointed_tags)
            return tag.get_image_url()
        return ''

    def get_site_logo(self):
        return self._try_extract()
