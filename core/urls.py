"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bot import views, pdf_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('webapp/', views.WebAppTemplateView.as_view(), name="list"),
    # path('webapp/', views.WebAppHomePage.as_view(), name="list"),
    path("webapp/<int:pk>/", views.WebAppDetailPage.as_view(), name="detail"),
    path("webapp/category/", views.WebAppCategoryPage.as_view(), name="by_category"),
    path('pdf/', pdf_views.generate_pdf2_view, name='generate_pdf2'),
    path('pdf/<int:pk>/', pdf_views.generate_pdf_view, name='generate_pdf'),
    path('generate-multiple-pdfs/', pdf_views.generate_multiple_pdfs_view, name='generate_multiple_pdfs'),
    # path("webapp/cart/", views.WebAppCartPage.as_view(), name="cart")
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += [path('', admin.site.urls),]