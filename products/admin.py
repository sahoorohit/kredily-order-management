from django.contrib import admin

from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'product_id',
        'name',
        'price',
        'available_quantity',
    ]
    readonly_fields = ['created_at', 'updated_at']
    fields = list_display + readonly_fields
