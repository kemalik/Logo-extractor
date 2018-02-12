from django.views.generic import TemplateView

from applications.page_parser.exceptions import BrowserClientException
from applications.page_parser.utils import BrowserClient


class ResultView(TemplateView):
    template_name = "result.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        client = BrowserClient()
        try:
            r = client.get_url_source('google.com')
        except BrowserClientException as e:
            context['error'] = e
            return context

        context['result'] = r
        return context
