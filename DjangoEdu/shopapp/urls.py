from django.urls import path

from .views import (ShopIndexView,
                    GroupListView,
                    # OrderListView,
                    orders_list,
                    create_product,
                    ProductDetaislView,
                    OrderDetailView,
                    ProductDeleteView,
                    ProductListView)

app_name = 'shopapp'

urlpatterns = [
    path ('', ShopIndexView.as_view(), name='index'),
    path ('groups/', GroupListView.as_view(), name='groups_list'),
    path ('products/', ProductListView.as_view(), name='products_list'),
    path ('products/<int:pk>/confirm-delete/', ProductDeleteView.as_view(), name='product_delete'),
    path ('products/<int:pk>', ProductDetaislView.as_view(), name='products_details'),
    path ('products/create', create_product, name='product_create'),
    # path ('orders/', OrderListView.as_view(), name='orders_list'),
    path ('orders/',orders_list, name='orders_list'),
    path ('orders/<int:pk>',OrderDetailView.as_view(), name='order_details'),
]

# products_list,
