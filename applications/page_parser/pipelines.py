from applications.page_parser.constants import *  # TODO change to named

from applications.page_parser.utils import HtmlTag


def check_attribute(tag: HtmlTag) -> HtmlTag:  # has attributes (class, id ...) keywords
    for attr in IMPORTANT_ATTRIBUTES:
        attribute_value = tag.get_attribute_value(attr)
        if not attribute_value:
            continue
        if any(word in attribute_value for word in LOGO_KEYWORDS):
            tag.add_point(PRIORITY_HIGH)

        if attr == ATTRIBUTE_NAME_HREF and any(word in attribute_value for word in IMPORTANT_URLS):
            tag.add_point(PRIORITY_MAJOR)
    return tag


def check_image_url(tag: HtmlTag) -> HtmlTag:  # has image url path keywords
    tag_image_url = tag.get_image_url()
    if not tag_image_url:
        tag.exclude()
        return tag
    if any(word in tag_image_url for word in LOGO_KEYWORDS):
        tag.add_point(PRIORITY_HIGH)
    return tag


def check_image_extension(tag: HtmlTag) -> HtmlTag:  # has image extension png, jpg, ...
    if any(tag.get_image_url().endswith(extension) for extension in IMPORTANT_FILE_EXTENSIONS):
        tag.add_point(PRIORITY_LOW)
    return tag


def check_image_size(tag: HtmlTag) -> HtmlTag:  # has image large, small size
    tag_size = tag.get_size()
    width, height = tag_size[SIZE_KEY_WIDTH], tag_size[SIZE_KEY_HEIGHT]

    if LOGO_MAX_WIDTH > width > LOGO_MIN_WIDTH and LOGO_MAX_HEIGHT > height > LOGO_MIN_HEIGHT:
        tag.add_point(PRIORITY_MINOR)
    return tag


def check_element_coordinates(tag: HtmlTag) -> HtmlTag:  # check element location in page by x, y
    coordinates = tag.get_coordinates()
    x, y = coordinates[COORDINATE_X], coordinates[COORDINATE_Y]
    if COORDINATE_Y_MIN < y < COORDINATE_Y_MAX and x > COORDINATE_X_MIN:
        tag.add_point(PRIORITY_MEDIUM)
    return tag


def check_element_parent(tag: HtmlTag) -> HtmlTag:  # is element in header, footer ...
    parent_tag = tag.get_parent_tag()
    while parent_tag.get_name() != TAG_NAME_BODY:
        for attr in IMPORTANT_ATTRIBUTES:
            attribute_value = parent_tag.get_attribute_value(attr)
            if not attribute_value:
                continue
            if any(word in attribute_value for word in LOGO_KEYWORDS):
                tag.add_point(PRIORITY_HIGH)
            if attr == ATTRIBUTE_NAME_HREF and any(attribute_value.endswith(url) for url in IMPORTANT_URLS):
                tag.add_point(PRIORITY_HIGH)

        parent_tag = parent_tag.get_parent_tag()
    return tag


def check_element_visibility(tag: HtmlTag) -> HtmlTag:  # is element visible ...
    if tag.is_visible():
        tag.add_point(PRIORITY_MEDIUM)
    return tag


point_pipeline = [
    check_image_url,
    check_attribute,
    check_image_extension,
    check_image_size,
    check_element_coordinates,
    check_element_parent,
    check_element_visibility,
]
