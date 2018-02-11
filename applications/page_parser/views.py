from django.views.generic import TemplateView

from applications.page_parser.utils import BrowserClient


class ResultView(TemplateView):
    template_name = "result.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        client = BrowserClient()

        r = client.get_url_source('http://google.com')

        context['result'] = r
        return context
