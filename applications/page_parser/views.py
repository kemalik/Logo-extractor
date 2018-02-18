import logging

from django.views.generic import TemplateView

from applications.page_parser.constants import ERROR_MESSAGE_ENTER_URL
from applications.page_parser.exceptions import LogoExtractorException
from applications.page_parser.utils import LogoExtractor

logger = logging.getLogger(__file__)


class ResultView(TemplateView):
    template_name = "result.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['error'] = ''

        url = self.request.GET.get('url')

        if not url:
            context['error'] = ERROR_MESSAGE_ENTER_URL
            return context
        logging.info('Got url: {}'.format(url))
        logo_extractor = LogoExtractor(url)

        try:
            context['result'] = logo_extractor.get_site_logo()
        except LogoExtractorException as e:
            logging.error(e)
            context['error'] = e

        return context
