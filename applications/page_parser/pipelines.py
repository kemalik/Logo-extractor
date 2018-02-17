def check_tag(tag):
    tag.add_point(1)
    return tag


def check_attribute(tag):  # has attributes (class, id ...) keywords
    important_attributes = ['id', 'class', 'alt']
    for attr in important_attributes:
        attribute_value = tag.get_attribute_value(attr)
        if not attribute_value:
            continue
        keywords = ['logo', 'ico']
        if any(word in attribute_value for word in keywords):
            tag.add_point(5)
    return tag


def check_image_url(tag):  # has image url keywords
    tag.add_point(1)
    return tag


def check_image_extension(tag):  # has image extension png, jpg, ...
    tag.add_point(1)
    return tag


def check_image_size(tag):  # has image large, small size
    tag.add_point(1)
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


def check_element_placement(tag):  # is element in top, bottom, ...
    tag.add_point(1)
    return tag


def check_element_coordinates(tag):  # check element location in page by x, y
    tag.add_point(1)
    return tag


def check_element_parent(tag):  # is element in header, footer ...
    tag.add_point(1)
    return tag


def check_element_visibility(tag):  # is element visible ...
    if tag.is_visible():
        tag.add_point(2)
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
    check_element_parent,
    check_element_visibility
]
