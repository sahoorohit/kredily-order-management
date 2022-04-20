from django.contrib import admin

from orders.models import Order, SubOrder


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_id',
        'amount',
        'customer',
        'created_at',
    ]
    readonly_fields = ['order_id', 'created_at', 'updated_at']
    fields = list_display


@admin.register(SubOrder)
class SubOrderAdmin(admin.ModelAdmin):
    pass
