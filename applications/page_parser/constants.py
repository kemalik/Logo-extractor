ERROR_MESSAGE_ENTER_URL = 'Please enter url'

XPATH_NOT_SCRIPT_STYLE_IMG = '//body//*[not(script|style|img)]'
XPATH_ALL_IMAGES = '//body//img'

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
SCRIPT_APPEND_CLASS_IMAGE_CONTAINERS = """
        var tags = document.getElementsByTagName('*'), el;
        for (var i = 0, len = tags.length; i < len; i++) {
            el = tags[i];
            if (document.defaultView.getComputedStyle(el, null).getPropertyValue('background-image') !== 'none')
                el.className += ' bg_found';
        }
        """