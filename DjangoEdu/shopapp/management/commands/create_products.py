from django.core.management import BaseCommand
from shopapp.models import Product


class Command(BaseCommand):
    """
    Creates products
    """
    def handle(self, *args, **options):
        self.stdout.write('Creating products')

        products_names = [
            'Laptop',
            'Desktop',
            'Smartphone',
        ]
        for product_name in products_names:
            product, created = Product.objects.get_or_create(name=product_name)
            self.stdout.write('Product {} created'.format(product_name))

        self.stdout.write( self.style.SUCCESS( "Products created." ) )
