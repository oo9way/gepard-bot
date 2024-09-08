from collections.abc import Callable, Sequence
from typing import Any
from django.contrib import admin
from django.http import HttpRequest
from bot.models import TelegramUser, Contact, Product, Order, OrderItem, CustomUser, Category, Area, ClientCategory
from solo.admin import SingletonModelAdmin
from django.db.models import Sum, F, FloatField
from django.db.models import Q
from django.utils.html import format_html


@admin.register(ClientCategory)
class ClientCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name", )


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
    list_display = ("id", "first_name", "last_name", "username", "is_agent", "phone", "category")
    list_display_links = ("id", "first_name", "last_name")
    list_editable = ("is_agent", )
    search_fields = ("first_name", "last_name", "username", "phone")
    readonly_fields = ("telegram_id", "phone")


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
    list_display = ("id", "user", "status",  "get_total_cost", "location_path")
    list_per_page = 20
    list_display_links = ("id", "user",)
    inlines = (OrderItemTabularInline, )
    fields = ("user", "status", "payment_status", "payment_type")
    list_filter = ("user", "agent", "user__territory",)
    search_fields = ("id",)
    date_hierarchy = "created_at"

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
            return ("id", "user", "status", "get_total_cost", "payment_status", "payment_type", "get_location", "created_at", "get_accountant_approve_time", "get_director_approve_time", "get_storekeeper_approve_time")
        
        if request.user.role == "director":
            return ("id", "user", "status", "get_total_cost", "payment_status", "payment_type", "get_location", "created_at", "get_accountant_approve_time", "get_director_approve_time", "get_storekeeper_approve_time")
        
        if request.user.role == "storekeeper":
            return ("id", "user", "status", "get_total_cost", "get_location",  "created_at", "get_accountant_approve_time", "get_director_approve_time", "get_storekeeper_approve_time")
        
        return ("id", "user", "status", "get_total_cost", "payment_status", "payment_type", "get_location", "created_at", "get_accountant_approve_time", "get_director_approve_time", "get_storekeeper_approve_time")

    def get_accountant_approve_time(self, obj):
        return format_html(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><circle cx="12" cy="12" r="12" fill="green"/><path fill="none" stroke="white" stroke-width="2" d="M6 12l4 4l8-8" /></svg> Подтвержденный <br>{obj.accountant_approve_time.strftime("%d.%m.%Y %H:%M:%S")}' if obj.accountant_approve_time else '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><circle cx="12" cy="12" r="12" fill="red"/><path fill="none" stroke="white" stroke-width="2" d="M6 6l12 12M6 18L18 6" /></svg>')

    get_accountant_approve_time.short_description = "Бухгалтер"

    def get_director_approve_time(self, obj):
        return format_html(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><circle cx="12" cy="12" r="12" fill="green"/><path fill="none" stroke="white" stroke-width="2" d="M6 12l4 4l8-8" /></svg> Подтвержденный <br>{obj.director_approve_time.strftime("%d.%m.%Y %H:%M:%S")}' if obj.director_approve_time else '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><circle cx="12" cy="12" r="12" fill="red"/><path fill="none" stroke="white" stroke-width="2" d="M6 6l12 12M6 18L18 6" /></svg>')


    get_director_approve_time.short_description = "Директор"

    def get_storekeeper_approve_time(self, obj):
        return format_html(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><circle cx="12" cy="12" r="12" fill="green"/><path fill="none" stroke="white" stroke-width="2" d="M6 12l4 4l8-8" /></svg> Подтвержденный <br>{obj.storekeeper_approve_time.strftime("%d.%m.%Y %H:%M:%S")}' if obj.storekeeper_approve_time else '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><circle cx="12" cy="12" r="12" fill="red"/><path fill="none" stroke="white" stroke-width="2" d="M6 6l12 12M6 18L18 6" /></svg>')


    get_storekeeper_approve_time.short_description = "Кладовщик"
    
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
        queryset = queryset.annotate(total_price=Sum(F('items__price_uzs') * F('items__qty'), output_field=FloatField()))
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

    def get_location(self, obj):
        if obj.location_path:
            return format_html(
                f"<a href='{obj.location_path}'>Посмотреть место доставки</a>"
            )
    get_location.short_description = "Место доставки"


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)
    search_fields = ("name",)