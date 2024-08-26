from django.views.generic import TemplateView, ListView
from bot.models import Product
from django.db.models import Q


class WebAppTemplateView(ListView):
    model = Product
    context_object_name = "products"
    template_name = 'webapp.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset