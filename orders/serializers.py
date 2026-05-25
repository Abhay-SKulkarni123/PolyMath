from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source='product.name',
        read_only=True
    )
    product_type = serializers.CharField(
        source='product.type',
        read_only=True
    )
    item_total = serializers.ReadOnlyField()
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product_name','product_type', 'quantity', 'price', 'item_total', 'download_url']

    def get_download_url(self, obj):
        if obj.download_token:
            return f'/api/orders/download/{obj.download_token}/'
        return None


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'status', 'total_price',
            'shipping_address', 'items',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'total_price', 'created_at', 'updated_at']


class CheckoutSerializer(serializers.Serializer):
    shipping_address = serializers.CharField()