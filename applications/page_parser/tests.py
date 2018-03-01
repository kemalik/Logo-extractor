from unittest.mock import Mock, patch

from django.test import TestCase

from applications.page_parser.constants import (
    CSS_PROPERTY_VALUE_NONE, CSS_PROPERTY_VALUE_HIDDEN, COORDINATE_Y, COORDINATE_X,
    ATTRIBUTE_NAME_SRC, TAG_NAME_BODY, PRIORITY_HIGH, PRIORITY_MAJOR, PRIORITY_LOW, PRIORITY_MINOR, PRIORITY_MEDIUM)
from applications.page_parser.exceptions import BrowserClientException
from applications.page_parser.pipelines import check_attribute, check_image_url, check_image_extension, \
    check_image_size, check_element_coordinates, check_element_parent, check_element_visibility
from applications.page_parser.utils import BrowserClient, HtmlTag, LogoExtractor


class HtmlTagTestCase(TestCase):
    def setUp(self):
        self.mocked_tag = Mock()
        self.test_image_url = 'http://example.com/img.png'
        self.html_tag = HtmlTag(tag=self.mocked_tag, is_image=True)

    def test_exclude_should_set_true_for_exclude_parameter(self):
        self.html_tag.exclude()

        self.assertEqual(self.html_tag.is_excluded(), True)

    def test_get_score_should_return_tag_score(self):
        self.assertEqual(self.html_tag.get_score(), 1)

    def test_get_score_should_return_zero_if_tag_excluded(self):
        expected_score = 0
        self.html_tag.exclude()
        self.assertEqual(self.html_tag.get_score(), expected_score)

    def test_add_score_should_add_value_to_score_parameter(self):
        expected_score = 6
        self.html_tag.add_score(PRIORITY_HIGH)
        self.assertEqual(self.html_tag.get_score(), expected_score)

    def test_get_image_url_should_return_attribute_src_if_it_image(self):
        expected_image_url = self.test_image_url
        self.mocked_tag.get_attribute.return_value = expected_image_url
        self.assertEqual(self.html_tag.get_image_url(), expected_image_url)

    def test_get_image_url_should_return_style_image_url_if_it_no_image(self):
        css_background_parameter = 'url("{image_url}")'.format(image_url=self.test_image_url)

        self.mocked_tag.value_of_css_property.return_value = css_background_parameter

        self.html_tag = HtmlTag(tag=self.mocked_tag, is_image=False)

        self.assertEqual(self.html_tag.get_image_url(), self.test_image_url)

    def test_get_image_url_should_return_none_if_no_has_image_url(self):
        css_background_parameter = CSS_PROPERTY_VALUE_NONE

        self.mocked_tag.value_of_css_property.return_value = css_background_parameter

        self.html_tag = HtmlTag(tag=self.mocked_tag, is_image=False)

        self.assertIsNone(self.html_tag.get_image_url())

    def test_is_visible_should_return_false_if_tag_has_display_none_style(self):
        self.mocked_tag.value_of_css_property.return_value = CSS_PROPERTY_VALUE_NONE

        self.assertFalse(self.html_tag.is_visible())

    def test_is_visible_should_return_false_if_tag_has_hidden_style(self):
        self.mocked_tag.value_of_css_property.return_value = CSS_PROPERTY_VALUE_HIDDEN

        self.assertFalse(self.html_tag.is_visible())

    def test_is_visible_should_return_true_if_tag_no_has_hide_styles(self):
        self.mocked_tag.value_of_css_property.return_value = None

        self.assertTrue(self.html_tag.is_visible())

    def test_get_size_should_return_tags_width_and_height_value(self):
        expected_tag_size = (100, 100)
        self.mocked_tag.size = expected_tag_size

        self.assertEqual(self.html_tag.get_size(), expected_tag_size)

    def test_get_coordinates_should_return_tags_coordinate_parameters(self):
        expected_tag_coordinates = {
            COORDINATE_X: 100,
            COORDINATE_Y: 100
        }
        self.mocked_tag.location = expected_tag_coordinates

        self.assertEqual(self.html_tag.get_coordinates(), expected_tag_coordinates)

    def test_get_parent_tag_should_return_tags_parent_element(self):
        expected_element = 'Parent element'
        self.mocked_tag.find_element_by_xpath.return_value = expected_element

        self.assertIsInstance(self.html_tag.get_parent_tag(), HtmlTag)

    def test_get_name_should_return_tags_name(self):
        expected_element_name = TAG_NAME_BODY
        self.mocked_tag.tag_name = expected_element_name

        self.assertEqual(self.html_tag.get_name(), expected_element_name)

    def test_get_attribute_value_should_return_tags_attribute_value(self):
        expected_attribute_value = self.test_image_url
        self.mocked_tag.get_attribute.return_value = expected_attribute_value

        self.assertEqual(self.html_tag.get_attribute_value(ATTRIBUTE_NAME_SRC), expected_attribute_value)


class BrowserClientTestCase(TestCase):
    @patch('selenium.webdriver.Remote')
    def setUp(self, driver):
        self.driver = driver
        self.test_url = 'htpp://google.com'
        self.browser_client = BrowserClient(url=self.test_url)
        self.browser_client.browser = self.driver

    @patch('selenium.webdriver.Remote')
    def test_constructor_should_raise_exception_if_cant_connect_to_selenium(self, driver):
        driver.side_effect = Exception

        self.assertRaises(BrowserClientException, lambda: BrowserClient(''))

    def test_get_url_source_should_return_page_source(self):
        expected_page_source = 'page source'
        self.driver.page_source = expected_page_source
        self.assertEqual(self.browser_client.get_url_source(), expected_page_source)

    def test_get_elements_by_xpath_should_return_list_elements_found_in_page_by_xpath(self):
        expected_elements = []
        self.driver.find_elements_by_xpath.return_value = expected_elements
        self.assertEqual(self.browser_client.get_elements_by_xpath(''), expected_elements)

    def test_get_elements_by_xpath_should_return_list_elements_found_by_class_name(self):
        expected_elements = []
        self.driver.find_elements_by_class_name.return_value = expected_elements
        self.assertEqual(self.browser_client.get_elements_by_class(''), expected_elements)

    def test_get_images_in_page_should_return_list_image_elements(self):
        expected_elements = []
        self.driver.find_elements_by_xpath.return_value = expected_elements
        self.assertEqual(self.browser_client.get_images_in_page(), expected_elements)

    def test_get_image_containers_should_return_list_elements_which_contains_image(self):
        expected_elements = []
        self.driver.find_elements_by_class_name.return_value = expected_elements
        self.assertEqual(self.browser_client.get_image_containers(), expected_elements)

    def test_get_potential_tags_should_return_list_elements_which_exactly_contains_image(self):
        expected_elements = []
        self.driver.find_elements_by_class_name.return_value = expected_elements
        self.driver.find_elements_by_xpath.return_value = expected_elements
        self.assertEqual(self.browser_client.get_potential_tags(), expected_elements)


class LogoExtractorTestCase(TestCase):
    def setUp(self):
        self.test_url = 'http://google.com'
        self.test_image_url = 'http://example.com/img.png'
        self.logo_extractor = LogoExtractor(self.test_url)

    @patch('applications.page_parser.utils.BrowserClient')
    @patch('applications.page_parser.pipelines.scoring_pipeline')
    def test_get_site_logo_should_return_logo_of_given_url(self, scoring_pipeline, browser_client):
        expected_image_url = self.test_image_url
        scoring_pipeline.__iter__.return_value = [lambda x: x]
        html_tag = Mock()

        html_tag.get_image_url.return_value = expected_image_url
        html_tag.get_score.return_value = 13

        browser_client_instance = Mock()
        browser_client.return_value = browser_client_instance
        browser_client_instance.get_potential_tags.return_value = [html_tag]
        self.assertEqual(self.logo_extractor.get_site_logo(), expected_image_url)

    @patch('selenium.webdriver.Remote')
    @patch('applications.page_parser.utils.BrowserClient.get_potential_tags')
    def test_get_site_logo_should_return_empty_string_if_cannt_find_logo(self, get_potential_tags, driver):
        expected_value = ''
        get_potential_tags.return_value = []
        self.assertEqual(self.logo_extractor.get_site_logo(), expected_value)


class PipelineTestCase(TestCase):
    def test_check_attribute_should_pass_add_point_if_not_contains_attributes(self):
        mocker_tag = Mock()
        mocker_tag.get_attribute.return_value = None
        html_tag = HtmlTag(tag=mocker_tag)

        self.assertEqual(check_attribute(html_tag), html_tag)

    def test_check_attribute_should_add_point_if_attributes_contains_keywords(self):
        mocker_tag = Mock()
        mocker_tag.get_attribute.return_value = 'logo'
        html_tag = HtmlTag(tag=mocker_tag)
        old_score = html_tag.get_score()
        expected_score = old_score + 20
        scored_tag = check_attribute(html_tag)
        self.assertEqual(scored_tag.get_score(), expected_score)

    def test_check_attribute_should_add_point_if_attributes_contains_keywords_in_any_case(self):
        mocker_tag = Mock()
        mocker_tag.get_attribute.return_value = 'LOGO'
        html_tag = HtmlTag(tag=mocker_tag)
        old_score = html_tag.get_score()
        expected_score = old_score + 20
        scored_tag = check_attribute(html_tag)
        self.assertEqual(scored_tag.get_score(), expected_score)

    def test_check_attribute_should_add_point_if_parent_is_link_and_contains_keywords(self):
        mocker_tag = Mock()
        mocker_tag.get_attribute.return_value = 'index.html'
        html_tag = HtmlTag(tag=mocker_tag)
        old_score = html_tag.get_score()
        expected_score = old_score + PRIORITY_MAJOR
        scored_tag = check_attribute(html_tag)
        self.assertEqual(scored_tag.get_score(), expected_score)

    def test_check_image_url_should_exclude_tag_if_no_has_image_url(self):
        mocker_tag = Mock()
        mocker_tag.get_attribute.return_value = None
        html_tag = HtmlTag(tag=mocker_tag, is_image=True)
        scored_tag = check_image_url(html_tag)
        self.assertTrue(scored_tag.is_excluded())

    def test_check_image_url_should_add_score_if_image_url_contains_keywords(self):
        mocker_tag = Mock()
        html_tag = HtmlTag(tag=mocker_tag, is_image=True)
        expected_score = html_tag.get_score() + PRIORITY_HIGH

        mocker_tag.get_attribute.return_value = 'logo'
        scored_tag = check_image_url(html_tag)
        self.assertEqual(scored_tag.get_score(), expected_score)

    def test_check_image_extension_should_add_score_if_image_url_contains_image_extesions(self):
        mocker_tag = Mock()
        html_tag = HtmlTag(tag=mocker_tag, is_image=True)
        expected_score = html_tag.get_score() + PRIORITY_LOW

        mocker_tag.get_attribute.return_value = 'image.png'
        scored_tag = check_image_extension(html_tag)
        self.assertEqual(scored_tag.get_score(), expected_score)

    def test_check_image_size_should_add_score_if_image_has_needed_size(self):
        mocker_tag = Mock()
        html_tag = HtmlTag(tag=mocker_tag, is_image=True)
        expected_score = html_tag.get_score() + PRIORITY_MINOR

        mocker_tag.size = {'width': 100, 'height': 100}
        scored_tag = check_image_size(html_tag)
        self.assertEqual(scored_tag.get_score(), expected_score)

    def test_check_element_coordinates_should_add_score_if_image_has_needed_coordinates_in_page(self):
        mocker_tag = Mock()
        html_tag = HtmlTag(tag=mocker_tag, is_image=True)
        expected_score = html_tag.get_score() + PRIORITY_MEDIUM

        mocker_tag.location = {'x': 100, 'y': 100}
        scored_tag = check_element_coordinates(html_tag)
        self.assertEqual(scored_tag.get_score(), expected_score)

    def test_check_element_parent_should_pass_if_parent_tags_no_have_attributes(self):
        mocker_tag = Mock()
        html_tag = HtmlTag(tag=mocker_tag, is_image=True)
        expected_score = html_tag.get_score()

        body_element = Mock()
        body_element.tag_name = 'body'

        parent_element = Mock()
        parent_element.tag_name = 'a'
        parent_element.get_attribute.return_value = None
        parent_element.find_element_by_xpath.return_value = body_element

        mocker_tag.find_element_by_xpath.return_value = parent_element

        scored_tag = check_element_parent(html_tag)
        self.assertEqual(scored_tag.get_score(), expected_score)

    def test_check_element_parent_should_add_score_if_parent_tags_attributes_have_keywords(self):
        mocker_tag = Mock()
        html_tag = HtmlTag(tag=mocker_tag, is_image=True)
        expected_score = html_tag.get_score() + 20

        body_element = Mock()
        body_element.tag_name = 'body'

        parent_element = Mock()
        parent_element.tag_name = 'a'
        parent_element.get_attribute.return_value = 'logo'
        parent_element.find_element_by_xpath.return_value = body_element

        mocker_tag.find_element_by_xpath.return_value = parent_element

        scored_tag = check_element_parent(html_tag)
        self.assertEqual(scored_tag.get_score(), expected_score)

    def test_check_element_parent_should_add_score_if_parent_link_attributes_have_keywords_urls(self):
        mocker_tag = Mock()
        html_tag = HtmlTag(tag=mocker_tag, is_image=True)
        expected_score = html_tag.get_score() + PRIORITY_HIGH

        body_element = Mock()
        body_element.tag_name = 'body'

        parent_element = Mock()
        parent_element.tag_name = 'a'
        parent_element.get_attribute.return_value = 'index.html'
        parent_element.find_element_by_xpath.return_value = body_element

        mocker_tag.find_element_by_xpath.return_value = parent_element

        scored_tag = check_element_parent(html_tag)
        self.assertEqual(scored_tag.get_score(), expected_score)

    def test_check_element_visibility_should_add_score_if_tag_visible_to_user(self):
        mocker_tag = Mock()
        html_tag = HtmlTag(tag=mocker_tag, is_image=True)
        expected_score = html_tag.get_score() + PRIORITY_MEDIUM

        mocker_tag.value_of_css_property.return_value = None

        scored_tag = check_element_visibility(html_tag)
        self.assertEqual(scored_tag.get_score(), expected_score)
