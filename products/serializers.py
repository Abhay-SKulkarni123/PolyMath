from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source='vendor.store_name', read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(many=True, write_only=True, queryset=Category.objects.all(), source='categories')
    
    class Meta:
        model = Product
        fields = [
            'id',
            'vendor_name',
            'categories',
            'category_ids',
            'name',
            'description',
            'price',
            'stock',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'vendor_name', 'created_at']