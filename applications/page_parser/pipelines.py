from applications.page_parser.constants import (
    IMPORTANT_ATTRIBUTES, LOGO_KEYWORDS, IMPORTANT_URLS, IMPORTANT_TAGS,
    IMPORTANT_FILE_EXTENSIONS,
    PRIORITY_HIGH, PRIORITY_MEDIUM, PRIORITY_LOW)

from applications.page_parser.utils import HtmlTag


def check_tag(tag):
    tag.add_point(1)
    return tag


def check_attribute(tag):  # has attributes (class, id ...) keywords
    for attr in IMPORTANT_ATTRIBUTES:
        attribute_value = tag.get_attribute_value(attr)
        if not attribute_value:
            continue
        if any(word in attribute_value for word in LOGO_KEYWORDS):
            tag.add_point(PRIORITY_HIGH)
    return tag


def check_image_url_name(tag: HtmlTag) -> HtmlTag:  # has image url path keywords
    tag_image_url = tag.get_image_url()
    if any(word in tag_image_url for word in LOGO_KEYWORDS):
        tag.add_point(PRIORITY_HIGH)
    return tag


def check_image_url(tag: HtmlTag) -> HtmlTag:  # has tag image url
    tag_image = tag.get_image_url()
    if not tag_image:
        tag.exclude()
        return tag
    tag.add_point(PRIORITY_HIGH)
    return tag


def check_image_extension(tag: HtmlTag) -> HtmlTag:  # has image extension png, jpg, ...
    if any(tag.get_image_url().endswith(extension) for extension in IMPORTANT_FILE_EXTENSIONS):
        tag.add_point(PRIORITY_LOW)
    return tag


def check_image_size(tag: HtmlTag) -> HtmlTag:  # has image large, small size
    tag_size = tag.get_size()
    width, height = tag_size['width'], tag_size['height']
    if 600 > width > 0 and 600 > height > 0:
        tag.add_point(PRIORITY_MEDIUM)
    return tag


def check_image_name(tag):  # has image file name keywords
    tag.add_point(1)
    return tag


def check_style(tag):  # has element css styles
    tag.add_point(1)
    return tag


def check_inline_style(tag):  # has element inline styles
    tag.add_point(1)
    return tag


def check_element_placement(tag: HtmlTag) -> HtmlTag:  # is element in header, footer, ...
    parent_tag = tag.get_parent_tag()
    while parent_tag.get_name() != 'body':
        if any(tag_name in parent_tag.get_name() for tag_name in IMPORTANT_TAGS):
            tag.add_point(PRIORITY_LOW)
        parent_tag = parent_tag.get_parent_tag()
    return tag


def check_element_coordinates(tag: HtmlTag) -> HtmlTag:  # check element location in page by x, y
    coordinates = tag.get_coordinates()
    x, y = coordinates['x'], coordinates['y']
    if 0 < x < 200 and y > 0:
        tag.add_point(PRIORITY_LOW)
    return tag


def check_element_parent(tag: HtmlTag) -> HtmlTag:  # is element in header, footer ...
    parent_tag = tag.get_parent_tag()
    while parent_tag.get_name() != 'body':
        if parent_tag.get_name() == 'a':
            tag.add_point(PRIORITY_LOW)
            if any(parent_tag.get_attribute_value('href').endswith(url) for url in IMPORTANT_URLS):
                tag.add_point(PRIORITY_HIGH)
        parent_tag = parent_tag.get_parent_tag()
    return tag


def check_element_visibility(tag):  # is element visible ...
    if tag.is_visible():
        tag.add_point(PRIORITY_HIGH)
    return tag


point_pipeline = [
    check_tag,
    check_attribute,
    check_image_url,
    check_image_extension,
    check_image_size,
    check_image_name,
    check_style,
    check_inline_style,
    check_element_placement,
    check_element_coordinates,
    check_element_parent,
    check_element_visibility,

]
