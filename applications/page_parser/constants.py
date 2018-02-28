ERROR_MESSAGE_ENTER_URL = 'Please enter url'

XPATH_NOT_SCRIPT_STYLE_IMG = '//body//*[not(script|style|img)]'
XPATH_ALL_IMAGES = '//body//img'
XPATH_PARENT_ELEMENT = '..'

REGEX_PATTERN_SUBSTRING_FROM_QUOTES = 'url\("([^"]*)"'

CSS_PROPERTY_BACKGROUND_IMAGE = 'background-image'
CSS_PROPERTY_DISPLAY = 'display'
CSS_PROPERTY_VISIBILITY = 'visibility'

CSS_PROPERTY_VALUE_NONE = 'none'
CSS_PROPERTY_VALUE_HIDDEN = 'hidden'

IMPORTANT_ATTRIBUTES = ['id', 'class', 'alt', 'href']
IMPORTANT_URLS = ['index', 'main', 'home']
IMPORTANT_TAGS = ['header', 'footer', 'a']
IMPORTANT_FILE_EXTENSIONS = ['.png', '.jpg', '.svg', '.gif', '.jpeg']

LOGO_KEYWORDS = ['logo']

PRIORITY_HIGH = 5
PRIORITY_MAJOR = 4
PRIORITY_MEDIUM = 3
PRIORITY_MINOR = 2
PRIORITY_LOW = 1

CONTEXT_RESULT_KEY = 'result'
CONTEXT_ERROR_KEY = 'error'
CONTEXT_URL_KEY = 'url'

SCRIPT_APPEND_CLASS_IMAGE_CONTAINERS = """
        var tags = document.getElementsByTagName('*'), el;
        for (var i = 0, len = tags.length; i < len; i++) {
            el = tags[i];
            if (document.defaultView.getComputedStyle(el, null).getPropertyValue('background-image') !== 'none')
                el.className += ' bg_found';
        }
        """
SIZE_KEY_HEIGHT = 'height'
SIZE_KEY_WIDTH = 'width'

ATTRIBUTE_NAME_HREF = 'href'
ATTRIBUTE_NAME_SRC = 'src'

TAG_NAME_BODY = 'body'

COORDINATE_X_MIN = 0
COORDINATE_Y_MAX = 200
COORDINATE_Y_MIN = 0
COORDINATE_Y = 'y'
COORDINATE_X = 'x'

LOGO_MIN_HEIGHT = 0
LOGO_MIN_WIDTH = 0
LOGO_MAX_WIDTH = 600
LOGO_MAX_HEIGHT = 600

CLASS_NAME_BG_ELEMENT = 'bg_found'
