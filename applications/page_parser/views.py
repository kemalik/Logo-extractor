import logging

from django.views.generic import TemplateView

from applications.page_parser.exceptions import LogoExtractorException
from applications.page_parser.utils import LogoExtractor

logger = logging.getLogger(__file__)


class ResultView(TemplateView):
    template_name = "result.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        url = self.request.GET.get('url')

        if not url:
            context['error'] = 'Please enter url'
            return context

        logo_extractor = LogoExtractor(url)

        try:
            result = logo_extractor.get_site_logo()
        except LogoExtractorException as e:
            logging.error(e)
            context['error'] = e
            return context

        context['result'] = result
        return context
