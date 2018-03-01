import logging
import re

from django.conf import settings
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from applications.page_parser.constants import (
    XPATH_ALL_IMAGES,
    REGEX_PATTERN_SUBSTRING_FROM_QUOTES, CSS_PROPERTY_BACKGROUND_IMAGE,
    CSS_PROPERTY_DISPLAY, CSS_PROPERTY_VISIBILITY, CSS_PROPERTY_VALUE_NONE, CSS_PROPERTY_VALUE_HIDDEN,
    SCRIPT_APPEND_CLASS_IMAGE_CONTAINERS, ATTRIBUTE_NAME_SRC, XPATH_PARENT_ELEMENT, CLASS_NAME_BG_ELEMENT)
from applications.page_parser.exceptions import BrowserClientException, LogoExtractorException

logger = logging.getLogger(__file__)


class HtmlTag(object):
    def __init__(self, tag, is_image=False):
        """
        Create new html tag with selenium web element than can be excluded
        from list and can be scored by pipeline checkers
        Args:
            tag (WebElement) : selenium web element
            is_image (bool) : True if current tag is image else False if tag is image container
        """
        self._is_image = is_image
        self._tag = tag
        self._score = 1
        self._excluded = False

    def _get_my_css_value(self, property_name: str):
        """
        Gets value of css property
        Args:
            property_name (str): name of css property

        Returns:
            str: value of css property
        """
        return self._tag.value_of_css_property(property_name)

    def exclude(self):
        """Exclude the tag"""
        self._excluded = True

    def is_excluded(self):
        """Returns whether element excluded"""
        return self._excluded

    def get_score(self):
        """
        Gets tag collected score
        Returns:
            int: zero if is excluded else value of score
        """
        if self._excluded:
            return 0
        return self._score

    def add_score(self, score: int) -> None:
        """
        Add score
        Args:
            score (int): value to add
        """
        self._score += score

    def _parse_url(self, text: str):
        """
        Retrieve image url from css parameter value
        Args:
            text (str): given css parameter value

        Returns:
            Image url if it parsed else ``None``
        """
        found = re.findall(REGEX_PATTERN_SUBSTRING_FROM_QUOTES, text)
        if found:
            return found[0]
        logging.warning('Style {} no have url'.format(text))
        return None

    def get_image_url(self):
        """
        Gets image url from tag
        Returns:
        str: image url from ``src`` attribute else try parse url from style
        """
        if self._is_image:
            return self._tag.get_attribute(ATTRIBUTE_NAME_SRC)

        css_value = self._get_my_css_value(CSS_PROPERTY_BACKGROUND_IMAGE)

        return self._parse_url(css_value)

    def is_visible(self):
        """
        Element is visible to user
        Returns:
            bool: True if no has hide styles else False
        """
        if self._get_my_css_value(CSS_PROPERTY_DISPLAY) == CSS_PROPERTY_VALUE_NONE:
            return False
        if self._get_my_css_value(CSS_PROPERTY_VISIBILITY) == CSS_PROPERTY_VALUE_HIDDEN:
            return False
        return True

    def get_size(self):
        """
        Gets tag size
        Returns:
            dict: With key ``width`` and ``height```
        """
        return self._tag.size

    def get_coordinates(self) -> dict:
        """
        Gets element placement coordinates in browser
        Returns:
            dict: with key ``x`` and ``y``
        """
        return self._tag.location

    def get_parent_tag(self):
        """
        Gets element parent tag by xpath
        Returns:
            HtmlTag: with current tag
        """
        parent_tag = self._tag.find_element_by_xpath(XPATH_PARENT_ELEMENT)
        return HtmlTag(parent_tag)

    def get_name(self):
        """
        Get tag name
        Returns:
            str: tag name
        """
        return self._tag.tag_name

    def get_attribute_value(self, attribute):
        """
        Gets current tag attribute value
        Args:
            attribute (str): attribute name

        Returns:
            str: attribute name if tag has
            None: if no has such attribute
        """
        return self._tag.get_attribute(attribute)


class BrowserClient(object):
    def __init__(self, url: str):
        """
        Initialize selenium web browser and open given url
        Args:
            url (str) : site url
        """
        self.browser = None
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
        """
        Opens url in browser
        """
        try:
            self.browser.get(url=self.url)
        except Exception as e:
            raise BrowserClientException(
                'Unable to open url {url}, {exception}'.format(url=self.url, exception=e)
            )

    def get_url_source(self):
        """
        Get page source
        Returns:
            str: page source code
        """
        return self.browser.page_source

    def get_elements_by_xpath(self, xpath):
        """
        Gets elements by xpath
        Args:
            xpath: The xpath regex of the elements to find

        Returns:
            list: list of WebElement - a list with elements if any was found.  An
           empty list if not
        """
        return self.browser.find_elements_by_xpath(xpath)

    def get_elements_by_class(self, class_name):
        """
        Gets elements by class name
        Args:
            class_name: The class name of the elements to find

        Returns:
            list: list of WebElement - a list with elements if any was found.  An
           empty list if not
        """
        return self.browser.find_elements_by_class_name(class_name)

    def get_images_in_page(self):
        """
        Find all img tags and make list of HtmlTag objects
        Returns:
            list: list of selenium web elements
        """
        images = self.get_elements_by_xpath(XPATH_ALL_IMAGES)

        images_in_page = [HtmlTag(tag=image, is_image=True) for image in images]

        return images_in_page

    def get_image_containers(self):
        """
        Gets image containers except img tag, that have background-image style parameters
        Returns:
            list: list of selenium web elements
        """
        self.browser.execute_script(SCRIPT_APPEND_CLASS_IMAGE_CONTAINERS)

        elements_with_bg_style = self.get_elements_by_class(CLASS_NAME_BG_ELEMENT)

        image_containers = [HtmlTag(tag=tag) for tag in elements_with_bg_style]

        return image_containers

    def get_potential_tags(self):
        """
        Get image tag and image container tags from page
        Returns:
            list: joined html tags
        """
        return self.get_images_in_page() + self.get_image_containers()

    def __del__(self):
        """
        Make quit if object destroyed
        """
        if self.browser:
            self.browser.quit()


class LogoExtractor(object):
    def __init__(self, url: str):
        """
        Initialize logo extractor
        Args:
            url (str): site url
        """
        self.url = url

    def _give_score_for_tag(self, tag: HtmlTag) -> HtmlTag:
        """
        Checks tag in cycle by each pipeline checkers, also html tag can be excluded by checker
        Args:
            tag (HtmlTag) : html tag that need check
        Returns:
            HtmlTag: checked html tag
        """
        from applications.page_parser.pipelines import scoring_pipeline
        for checker in scoring_pipeline:
            tag = checker(tag)
            if tag.is_excluded():
                break
        logging.info('Image url: {} score: {} '.format(tag.get_image_url(), tag.get_score()))
        return tag

    def _get_max_scored_image(self, scored_tags: list):
        """
        Gets maximum scored html tag
        Args:
            scored_tags (list): list of html tags
        Returns:
            HtmlTag: maximum scored tag
        """
        return max(scored_tags, key=lambda item: item.get_score())

    def get_site_logo(self):
        """
        Initialize selenium browser client and tries get potential tags that can be contain site logo
        Returns:
            str: site logo that scored with maximum point else empty string if logo not found
        """
        try:
            browser_client = BrowserClient(self.url)
            logging.info('Browser client initialized')
            result = browser_client.get_potential_tags()
        except BrowserClientException as e:
            logging.error(e)
            raise LogoExtractorException(e)

        if result:
            scored_tags = list(map(self._give_score_for_tag, result))

            tag = self._get_max_scored_image(scored_tags)
            return tag.get_image_url()
        return ''
