# from email.policy import default
from timeit import default_timer

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import Group

from .models import Product, Order
from .forms import ProductForm


def shop_index(request: HttpRequest):
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


def groups_list(request: HttpRequest):
    context = {
        # 'groups': Group.objects.all(),
        'groups': Group.objects.prefetch_related ( 'permissions' ).all ()
    }
    return render ( request, template_name="shopapp/shop-groups.html", context=context )


def products_list(request: HttpRequest):
    context = {
        'products': Product.objects.all (),
    }
    return render ( request, template_name="shopapp/products-list.html", context=context )

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
        'orders': Order.objects.select_related ( 'user' ).prefetch_related('products').all (),
    }
    return render ( request, template_name="shopapp/orders-list.html", context=context )
