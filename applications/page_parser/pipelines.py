def check_tag():
    pass


def check_attribute():  # has attributes (class, id ...) keywords
    pass


def check_image_url():  # has image url keywords
    pass


def check_image_extension():  # has image extension png, jpg, ...
    pass


def check_image_size():  # has image large, small size
    pass


def check_image_name():  # has image file name keywords
    pass


def check_style():  # has element css styles
    pass


def check_inline_style():  # has element inline styles
    pass


def check_element_placement():  # is element in top, bottom, ...
    pass


def check_element_coordinates():  # check element location in page by x, y
    pass


def check_element_parent():  # is element in header, footer ...
    pass


def check_element_visibility():  # is element visible ...
    pass


pipeline = [
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
