from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import path
from shopapp.common import save_csv_products

from .models import Product, Order
from .admin_mixins import ExportAsMixin
from .forms import CSVImportForm

class OrderInline(admin.TabularInline):
    model = Product.orders.through

@admin.action(description='Archive products')
def mark_archived(modeladmin: admin.ModelAdmin, request:HttpRequest, queryset:QuerySet):
    queryset.update(archived=True)

@admin.action(description='UnArchive products')
def mark_unarchived(modeladmin: admin.ModelAdmin, request:HttpRequest, queryset:QuerySet):
    queryset.update(archived=False)

@admin.register ( Product )
class ProductAdmin ( admin.ModelAdmin, ExportAsMixin ):
    actions = (
        mark_archived,
        mark_unarchived,
        'export_csv',
    )
    inlines = [
        OrderInline,
    ]
    list_display = ('pk', 'name', 'description_short', 'price', 'discount','archived')
    list_display_links = ('name', 'pk')
    ordering = ('-pk',)
    search_fields = ('name', 'description')
    fieldsets = [
        (None, {
            'fields': ('name', 'description',)
        }),
        ('Price options', {
            'fields': ('price', 'discount',),
            'classes': ('collapse', 'wide')
        }),
        ('Extra fields', {
            'classes': ('collapse', 'wide'),
            'fields': ('archived',),
            'description': ('Extra fields description'),
        })
    ]

    def description_short(self, obj: Product) -> str:
        if obj.description is None:
            return 'no description'
        if len ( obj.description ) > 48:
            return obj.description[:48] + '...'
        return obj.description

    change_list_template = 'shopapp/products_changelist.html'

    def import_csv(self, request: HttpRequest) -> HttpResponse:

        if request.method == 'GET':
            form = CSVImportForm()
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context)

        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                'form': form,
            }
            return render ( request, 'admin/csv_form.html', context, status=400 )

        save_csv_products (
            file=form.files['csv_file'].file,
            encoding=request.encoding,
        )

        # self.message_user(request, 'Successfully imported %d products.' % len(products))
        self.message_user(request, 'Successfully imported %d products.' )
        return redirect("..")

    def  get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('import-products-csv/',
                 self.import_csv,
                 name="import_products_csv"),
        ]
        return new_urls + urls


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
