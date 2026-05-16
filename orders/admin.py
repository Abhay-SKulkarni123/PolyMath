from django.contrib import admin
from .models import Order, OrderItem

class OrderItemline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['price', 'item_total']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_price', 'created_at']
    list_filter = ['status']
    search_fields = ['user__email']
    readonly_fields = ['total_price', 'created_at', 'updated_at']
    inlines = [OrderItemline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']