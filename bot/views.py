from django.views.generic import TemplateView, ListView
from bot.models import Product

class WebAppTemplateView(ListView):
    model = Product
    context_object_name = "products"
    template_name = 'webapp.html'