from typing import Sequence

from django.core.management import BaseCommand
from django.contrib.auth.models import User
from shopapp.models import Order, Product
from django.db import transaction


class Command ( BaseCommand ):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write ( 'Create order with product' )
        user = User.objects.get ( username='admin' )
        products: Sequence[Product] = Product.objects.all()
        order, created = Order.objects.get_or_create (
            delivery_address='ul Ivanova, d 8',
            promocode='Promo3',
            user=user, )
        for product in products:
            order.products.add(product)
        self.stdout.write ( f'Order created {order}' )
