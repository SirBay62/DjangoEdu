from django.contrib import admin

from .models import Product


@admin.register ( Product )
class ProductAdmin ( admin.ModelAdmin ):
    # list_display = ('pk', 'name', 'description', 'price', 'discount')
    list_display = ('pk', 'name', 'description_short', 'price', 'discount')
    list_display_links = ('name', 'pk')

    def description_short(self, obj: Product) -> str:
        if obj.description is None:
            return 'no description'
        if len ( obj.description ) > 48:
            return obj.description[:48] + '...'
        return obj.description

# admin.site.register ( Product, ProductAdmin )
