class BrowserClientException(Exception):
    def __init__(self, message):
        self.message = message


class LogoExtractorException(Exception):
    def __init__(self, message):
        self.message = message
