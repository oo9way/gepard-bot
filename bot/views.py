from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import TemplateView, ListView, DetailView
from bot.models import Product, Category, TelegramUser
from django.db.models import Q, F



class WebAppTemplateView(ListView):
    model = Product
    context_object_name = "products"
    template_name = 'webapp.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        user_id= self.request.GET.get("user_id", None)

        if query:
            queryset = queryset.filter(title__icontains=query)
        
        if user_id and user_id != "None":
            category = TelegramUser.objects.get(pk=user_id).category

            if category:
                queryset = queryset.extra(
                    select={
                        'price_uzs': f'price_uzs_{category}',
                        'price_usd': f'price_usd_{category}'
                    }
                )

            else:
                queryset = queryset.extra(
                    select={
                        'price_uzs': f'price_uzs_a',
                        'price_usd': f'price_usd_a'
                    }
                )

        else:
            queryset = queryset.extra(
                    select={
                        'price_uzs': f'price_uzs_a',
                        'price_usd': f'price_usd_a'
                    }
                )
            
        cat = self.request.GET.get("cate", None)
        if cat and (not user_id or user_id == "None"):
            queryset = queryset.extra(
                select={
                    'price_uzs': f'price_uzs_{cat}',
                    'price_usd': f'price_usd_{cat}'
                }
            )

        return queryset
    
    def get_context_data(self, **kwargs: Any):
        context =  super().get_context_data(**kwargs)
        context['user_id'] = self.request.GET.get("user_id", None)
        context['cate'] = self.request.GET.get("cate", "a")
        context['preview'] = self.request.GET.get("preview") == "1"
        context['categories'] = Category.objects.all()
        context['top'] = Product.objects.filter(is_top=True)
        context['prev_val'] = self.request.GET.get("preview")
        return context
    

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
        context['prev_val'] = self.request.GET.get("preview")
        return context


class WebAppCategoryPage(ListView):
    model = Product
    context_object_name = "products"
    template_name = "category.html"

    def get_queryset(self) -> QuerySet[Any]:
        category = self.request.GET.get("cat")
        queryset = super().get_queryset().filter(category_id=category)
        user_id = self.request.GET.get("user_id", None)

        if user_id and user_id != "None":
            category = TelegramUser.objects.get(pk=user_id).category

            if category:
                queryset = queryset.extra(
                    select={
                        'price_uzs': f'price_uzs_{category}',
                        'price_usd': f'price_usd_{category}'
                    }
                )
            else:
                queryset = queryset.extra(
                    select={
                        'price_uzs': f'price_uzs_a',
                        'price_usd': f'price_usd_a'
                    }
                )

        else:
            queryset = queryset.extra(
                    select={
                        'price_uzs': f'price_uzs_a',
                        'price_usd': f'price_usd_a'
                    }
                )

        cat = self.request.GET.get("cate", None)
        if cat and (not user_id or user_id == "None"):
            queryset = queryset.extra(
                select={
                    'price_uzs': f'price_uzs_{cat}',
                    'price_usd': f'price_usd_{cat}'
                }
            )

        return queryset
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user_id'] = self.request.GET.get("user_id", None)
        context['cate'] = self.request.GET.get("cate", "a")
        context['preview'] = self.request.GET.get("preview") == "1"
        context['prev_val'] = self.request.GET.get("preview")
        return context
    

class WebAppDetailPage(DetailView):
    template_name = "single.html"
    model = Product

    def get_queryset(self) -> QuerySet[Any]:
        user_id = self.request.GET.get("user_id", None)
        queryset = super().get_queryset()

        if user_id and user_id != "None":
            category = TelegramUser.objects.get(pk=user_id).category

            if category:
                queryset = queryset.extra(
                    select={
                        'price_uzs': f'price_uzs_{category}',
                        'price_usd': f'price_usd_{category}'
                    }
                )
            else:
                queryset = queryset.extra(
                    select={
                        'price_uzs': f'price_uzs_a',
                        'price_usd': f'price_usd_a'
                    }
                )

        else:
            queryset = queryset.extra(
                    select={
                        'price_uzs': f'price_uzs_a',
                        'price_usd': f'price_usd_a'
                    }
                )
            
        cat = self.request.GET.get("cate", None)
        if cat and (not user_id or user_id == "None"):
            queryset = queryset.extra(
                select={
                    'price_uzs': f'price_uzs_{cat}',
                    'price_usd': f'price_usd_{cat}'
                }
            )
        return queryset
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user_id'] = self.request.GET.get("user_id", None)
        context['cate'] = self.request.GET.get("cate", "a")
        context['preview'] = self.request.GET.get("preview") == "1"
        context['prev_val'] = self.request.GET.get("preview")
        return context



class WebAppCartPage(TemplateView):
    template_name = "app/product-backet.html"