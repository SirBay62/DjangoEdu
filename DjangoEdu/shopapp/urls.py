from django.urls import path

from .views import (ShopIndexView, GroupListView,
                  orders_list, create_product, ProductDetaislView, ProductListView)

app_name = 'shopapp'
urlpatterns = [
    path ('', ShopIndexView.as_view(), name='index'),
    path ('groups/', GroupListView.as_view(), name='groups_list'),
    path ('products/', ProductListView.as_view(), name='products_list'),
    path ('products/<int:pk>', ProductDetaislView.as_view(), name='products_details'),
    path ('products/create', create_product, name='product_create'),
    path ('orders/', orders_list, name='orders_list'),
]

# products_list,
