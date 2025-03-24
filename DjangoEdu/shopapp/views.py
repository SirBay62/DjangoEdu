"""
В этом модуле лежат различные наборы представлений
"""
from dataclasses import fields, field
from symtable import Class
from timeit import default_timer

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.views.generic import (TemplateView, ListView, DetailView, CreateView,
                                  UpdateView, DeleteView)

from csv import DictWriter

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse


from .models import Product, Order
from .forms import GroupsForm
from .forms import ProductForm
from .serialazers import ProductSerializer

from django.views import View

@extend_schema(description='Product views CRUD')
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product
    Полный CRUD для сущностей товара
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ['name', 'description']
    filterset_fields = [
        'name',
        'description',
        'price',
        'discount',
        'archived'
    ]
    ordering_fields = [
        'id',
        'name',
        'description',
        'price',
    ]

    @extend_schema(
        summary='Get one product by id',
        description='Retrieve one **product**, return 404 if not found',
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description='Product not found. Empty response.'),
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def download(self, request: Request):
        response = HttpResponse ( content_type='text/csv' )
        filename = 'products-export.csv'
        response['Content-Disposition'] = f'attachment; filename={filename}'
        queryset = self.filter_queryset ( self.get_queryset () )
        fields = [
            'name',
            'description',
            'price',
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response,fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })

        return response


class ShopIndexView(View):
    def get(self, request: HttpRequest)->HttpResponse:
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        context = {
            "time_running": default_timer (),
            "products": products,
        }
        return render ( request, "shopapp/shop-index.html", context=context )

class GroupListView(View):
    def get(self, request: HttpRequest)->HttpResponse:
        context = {
            # 'groups': Group.objects.all(),
            'form': GroupsForm(),
            'groups': Group.objects.prefetch_related ( 'permissions' ).all ()
        }
        return render ( request, template_name="shopapp/shop-groups.html", context=context )

    def post(self, request: HttpRequest)->HttpResponse:
        form = GroupsForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)

class ProductDetaislView(DetailView):
    template_name = "shopapp/product-details.html"
    model = Product
    context_object_name = "product"

# class ProductListView(TemplateView):
#     template_name = "shopapp/products-list.html"
#
#     def get_context_data(self, **kwargs):
#         context = super(ProductListView, self).get_context_data(**kwargs)
#         context['products'] = Product.objects.all()
#         return context

class ProductListView(ListView):
    template_name = "shopapp/products-list.html"
    model = Product
    context_object_name = "products"

# def products_list(request: HttpRequest):
#     context = {
#         'products': Product.objects.all (),
#     }
#     return render ( request, template_name="shopapp/products-list.html", context=context )

def create_product(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            # Product.objects.create(**form.cleaned_data)
            form.save()
            url = reverse ( 'shopapp:products_list' )
            return redirect (url)
    else:
        form = ProductForm()
    context = {
        'form': form,
    }

    return render ( request, template_name="shopapp/create-product.html", context=context )

def orders_list(request: HttpRequest):
    context = {
        'orders':
        Order.objects
        .select_related ( 'user' )
        .prefetch_related('products').all (),
    }

    return render ( request, template_name="shopapp/order_list.html", context=context )

# class OrderListView(ListView):
#     template_name = "shopapp/order_list.html"
#     queryset = {
#         Order.objects.all()
#         # .select_related ( 'user' )
#         # .prefetch_related ( 'products').all (),
#     }
#     # context_object_name = "orders"

class OrderDetailView(DetailView):
    template_name = "shopapp/order_details.html"
    # queryset = {
    #     Order.objects
    #     .select_related ( 'user' )
    #     .prefetch_related ( 'products')
    # }
    #
    # context_object_name = "orders"

    model = Order
    context_object_name = "order"

class ProductDeleteView(DeleteView):
    template_name = "shopapp/product_confirm_delete.html"
    model = Product
    success_url = reverse_lazy('shopapp:products_list')
