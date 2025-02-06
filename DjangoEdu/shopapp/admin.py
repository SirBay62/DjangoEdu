from django.contrib import admin

from .models import Product, Order


@admin.register ( Product )
class ProductAdmin ( admin.ModelAdmin ):
    # list_display = ('pk', 'name', 'description', 'price', 'discount')
    list_display = ('pk', 'name', 'description_short', 'price', 'discount')
    list_display_links = ('name', 'pk')
    ordering = ('-pk',)
    search_fields = ('name', 'description')

    def description_short(self, obj: Product) -> str:
        if obj.description is None:
            return 'no description'
        if len ( obj.description ) > 48:
            return obj.description[:48] + '...'
        return obj.description

# class ProductInline(admin.TabularInline):
class ProductInline(admin.StackedInline):
    model = Order.products.through

@admin.register ( Order )
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]

    list_display = 'delivery_address', 'promocode', 'created_at', 'user_verbose'

    def get_queryset(self, request):
        return Order.objects.select_related( 'user' ).prefetch_related('products')

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username

# admin.site.register ( Product, ProductAdmin )
