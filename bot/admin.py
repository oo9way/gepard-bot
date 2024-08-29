from collections.abc import Callable, Sequence
from typing import Any
from django.contrib import admin
from django.http import HttpRequest
from bot.models import TelegramUser, Contact, Product, Order, OrderItem, CustomUser, Category
from solo.admin import SingletonModelAdmin
from django.db.models import Sum, F, FloatField
from django.db.models import Q


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "cover")
    search_fields = ("title",)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "role", )
    fields = ("username", "first_name", "last_name", "role")

    def get_fields(self, request: HttpRequest, obj=None):
        if not obj:
            return ("username", "first_name", "last_name", "role", "password")
        return super().get_fields(request, obj)
    
    def has_delete_permission(self, request: HttpRequest, obj=None):
        if obj and obj.is_superuser and not request.user.is_superuser:
            return False
        return True

    

admin.site.register(Contact, SingletonModelAdmin)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "price_uzs", "price_usd")
    list_editable = ('is_active', )


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "username", "is_agent", "phone")
    list_display_links = ("id", "first_name", "last_name")
    list_editable = ("is_agent", )
    readonly_fields = ("telegram_id", "first_name", "last_name", "username", "phone")

class OrderItemTabularInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    
    def has_delete_permission(self, request, obj=None) -> bool:
        return False
    
    def has_change_permission(self, request: HttpRequest, obj=None) -> bool:
        return False
    
    def has_add_permission(self, *args):
        return False    


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status",  "get_total_cost")
    list_per_page = 20
    list_display_links = ("id", "user",)
    inlines = (OrderItemTabularInline, )
    fields = ("user", "status", "payment_status", "payment_type")

    def get_readonly_fields(self, request, obj=None):
        if request.user.role == "accountant":
            if obj.status != "pending":
                return ("status", "user")
            return ("user", )
            
        if request.user.role == "director":
            if obj.status != "approved_by_account":
                return ("status", "user", "payment_status", "payment_type")
            return ("user", )
        
        if request.user.role == "storekeeper":
            if obj.status != "approved_by_director":
                return ("status", "user")
            return ("user", )
            
        return super().get_readonly_fields(request, obj)
    
    def get_fields(self, request: HttpRequest, obj: Any | None = ...) -> Sequence[Callable[..., Any] | str]:
        if request.user.role == "storekeeper":
            return ("status", "user",)
        return super().get_fields(request, obj)


    def get_list_display(self, request):
        if request.user.role == "accountant":
            return ("id", "user", "status", "get_total_cost", "payment_status", "payment_type", "created_at", "accountant_approve_time", "director_approve_time", "storekeeper_approve_time")
        
        if request.user.role == "director":
            return ("id", "user", "status", "get_total_cost", "payment_status", "payment_type", "created_at", "accountant_approve_time", "director_approve_time", "storekeeper_approve_time")
        
        if request.user.role == "storekeeper":
            return ("id", "user", "status", "get_total_cost", "created_at", "accountant_approve_time", "director_approve_time", "storekeeper_approve_time")
        
        return ("id", "user", "status", "get_total_cost", "payment_status", "payment_type", "created_at", "accountant_approve_time", "director_approve_time", "storekeeper_approve_time")

        

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'status':
            if request.user.role == "accountant":
                kwargs['choices'] = Order.AccountantStatus.choices 
            elif request.user.role == "director":
                kwargs['choices'] = Order.DirectorStatus.choices
            else:
                kwargs['choices'] = Order.StoreKeeperStatus.choices

        return super().formfield_for_choice_field(db_field, request, **kwargs)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(total_price=Sum(F('items__price') * F('items__qty'), output_field=FloatField()))
        if request.user.role == "director":
            queryset = queryset.exclude(status="pending")

        if request.user.role == "storekeeper":
            queryset = queryset.exclude(Q(status="pending") | Q(status="approved_by_account"))
        return queryset
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request):
        return False    


    def get_total_cost(self, obj):
        return obj.total_price if obj.total_price else 0
    
    get_total_cost.short_description = "Umumiy summa"