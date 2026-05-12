from django.contrib import admin
from .models import Product, Category

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display= ['name', 'created_at']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display= ['name', 'vendor', 'price', 'stock', 'is_active']
    list_filter = ['is_active', 'categories']
    search_fields = ['name', 'vendor__store_name']

