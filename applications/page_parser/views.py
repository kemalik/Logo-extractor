import logging

from django.views.generic import TemplateView

from applications.page_parser.exceptions import BrowserClientException
from applications.page_parser.utils import BrowserClient

logger = logging.getLogger(__file__)


class ResultView(TemplateView):
    template_name = "result.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        client = BrowserClient()
        logging.debug('Browser client initialized')

        try:
            r = client.get_url_source('https://google.com')
        except BrowserClientException as e:
            logging.error(e)
            context['error'] = e
            return context

        context['result'] = r
        return context
