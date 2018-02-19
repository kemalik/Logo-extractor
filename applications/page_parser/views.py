import logging

from django.views.generic import TemplateView

from applications.page_parser.constants import (
    ERROR_MESSAGE_ENTER_URL, CONTEXT_RESULT_KEY, CONTEXT_ERROR_KEY
)
from applications.page_parser.exceptions import LogoExtractorException
from applications.page_parser.utils import LogoExtractor

logger = logging.getLogger(__file__)


class ResultView(TemplateView):
    template_name = "result.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[CONTEXT_ERROR_KEY] = ''

        url = self.request.GET.get('url')

        if not url:
            context[CONTEXT_ERROR_KEY] = ERROR_MESSAGE_ENTER_URL
            return context
        logging.info('Got url: {}'.format(url))
        logo_extractor = LogoExtractor(url)

        try:
            context[CONTEXT_RESULT_KEY] = logo_extractor.get_site_logo()
        except LogoExtractorException as e:
            logging.error(e)
            context[CONTEXT_ERROR_KEY] = e
        context['url'] = url
        return context
