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

        url = self.request.GET.get('url')

        if not url:
            context['error'] = 'Please enter url'
            return context

        try:
            result = client.get_url_source(url)
        except BrowserClientException as e:
            logging.error(e)
            context['error'] = e
            return context

        context['result'] = result
        return context
