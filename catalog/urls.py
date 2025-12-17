from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("business-essentials/", views.business_essentials, name="business_essentials"),
    path("<slug:category_slug>/", views.subcategory_list, name="subcategory_list"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("<slug:category_slug>/<slug:subcategory_slug>/", views.product_list, name="product_list"),
]
