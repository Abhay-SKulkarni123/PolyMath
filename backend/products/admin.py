from django.contrib import admin
from .models import KnowledgeField, Product

@admin.register(KnowledgeField)
class KnowledgeFieldAdmin(admin.ModelAdmin):
    list_display= ['icon', 'name', 'slug', 'color', 'created_at']
    search_fields = ['name']
    populated_fields = {'slug' : ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display= ['name', 'vendor', 'type', 'price', 'stock', 'is_active']
    list_filter = ['is_active', 'type', 'knowledge_fields']
    search_fields = ['name', 'vendor__store_name']
    filter_horizontal = ['knowledge_fields']

