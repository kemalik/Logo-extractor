from django.views.generic import TemplateView


class ResultView(TemplateView):
    template_name = "result.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['result'] = 'Hello world'
        return context
