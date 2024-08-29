from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import TemplateView, ListView, DetailView
from bot.models import Product, Category
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
    

class WebAppHomePage(ListView):
    model = Product
    context_object_name = "products"
    template_name = "app/index.html"

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_top=False)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset
    
    def get_context_data(self, **kwargs: Any):
        context =  super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['top'] = Product.objects.filter(is_top=True)
        return context


class WebAppDetailPage(DetailView):
    template_name = "app/product-detail.html"
    model = Product


class WebAppCartPage(TemplateView):
    template_name = "app/product-backet.html"