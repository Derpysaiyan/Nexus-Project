from django.contrib import admin
from django.urls import path
from store import views

urlpatterns = [
    path("admin/", admin.site.urls),

    
    path("", views.product_list_clean, name="product_list"),

    path("products/<int:product_id>/", views.product_detail, name="product_detail"),
    path("cart/", views.view_cart, name="view_cart"),
    path("cart/add/<int:sku_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),

   
]


