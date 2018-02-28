from django.test import TestCase
from unittest.mock import Mock

from applications.page_parser.constants import CSS_PROPERTY_VALUE_NONE, CSS_PROPERTY_VALUE_HIDDEN, COORDINATE_Y, \
    COORDINATE_X
from .utils import HtmlTag


class HtmlTagTestCase(TestCase):
    def setUp(self):
        self.mocked_tag = Mock()
        self.html_tag = HtmlTag(tag=self.mocked_tag, is_image=True)

    def test_exclude_should_set_true_for_exclude_parameter(self):
        self.html_tag.exclude()

        self.assertEqual(self.html_tag.is_excluded(), True)

    def test_get_score_should_return_tag_score(self):
        self.assertEqual(self.html_tag.get_score(), 1)

    def test_get_score_should_return_zero_if_tag_excluded(self):
        self.html_tag.exclude()
        self.assertEqual(self.html_tag.get_score(), 0)

    def test_add_score_should_add_value_to_score_parameter(self):
        self.html_tag.add_score(5)
        self.assertEqual(self.html_tag.get_score(), 6)

    def test_get_image_url_should_return_attribute_src_if_it_image(self):
        url = 'http://example.com'
        self.mocked_tag.get_attribute.return_value = url
        self.assertEqual(self.html_tag.get_image_url(), url)

    def test_get_image_url_should_return_style_image_url_if_it_no_image(self):
        image_url = 'http://example.com/img.png'
        css_background_parameter = 'url("{image_url}")'.format(image_url=image_url)

        self.mocked_tag.value_of_css_property.return_value = css_background_parameter

        self.html_tag = HtmlTag(tag=self.mocked_tag, is_image=False)

        self.assertEqual(self.html_tag.get_image_url(), image_url)

    def test_get_image_url_should_return_none_if_no_has_image_url(self):
        css_background_parameter = 'none'

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
        expected_element_name = 'div'
        self.mocked_tag.tag_name = expected_element_name

        self.assertEqual(self.html_tag.get_name(), expected_element_name)

    def test_get_attribute_value_should_return_tags_attribute_value(self):
        expected_attribute_value = 'http://example.com/img.png'
        self.mocked_tag.get_attribute.return_value = expected_attribute_value

        self.assertEqual(self.html_tag.get_attribute_value('src'), expected_attribute_value)

