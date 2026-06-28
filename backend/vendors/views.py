from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Sum, Count, Q
from products.models import Product
from orders.models import Order, OrderItem
from core.permissions import IsVendor

class VendorStatsView(APIView):
    permission_classes = [IsAuthenticated, IsVendor]

    def get(self, request):
        try:
            vendor = request.user.vendorprofile
        except:
            return Response({'error': 'No vendor profile'}, status=status.HTTP_400_BAD_REQUEST)

        # Total revenue from completed orders
        orders = Order.objects.filter(
            items__product__vendor=vendor,
            status='completed'
        ).distinct()
        
        total_revenue = sum(float(order.total_price) for order in orders)
        
        # Product count
        product_count = Product.objects.filter(vendor=vendor).count()
        
        # Order count
        order_count = orders.count()
        
        # Pending orders
        pending_count = Order.objects.filter(
            items__product__vendor=vendor,
            status='pending'
        ).distinct().count()

        return Response({
            'total_revenue': f"{total_revenue:.2f}",
            'total_products': product_count,
            'total_orders': order_count,
            'pending_orders': pending_count,
        })


class VendorProductsView(APIView):
    permission_classes = [IsAuthenticated, IsVendor]

    def get(self, request):
        try:
            vendor = request.user.vendorprofile
        except:
            return Response({'error': 'No vendor profile'}, status=status.HTTP_400_BAD_REQUEST)

        products = Product.objects.filter(vendor=vendor).values(
            'id', 'name', 'price', 'type', 'stock', 'is_active', 'created_at'
        ).order_by('-created_at')

        return Response({
            'count': products.count(),
            'results': list(products)
        })


class VendorOrdersView(APIView):
    permission_classes = [IsAuthenticated, IsVendor]

    def get(self, request):
        try:
            vendor = request.user.vendorprofile
        except:
            return Response({'error': 'No vendor profile'}, status=status.HTTP_400_BAD_REQUEST)

        orders = Order.objects.filter(
            items__product__vendor=vendor
        ).distinct().values(
            'id', 'status', 'total_price', 'created_at'
        ).order_by('-created_at')

        results = []
        for order in orders:
            items_count = OrderItem.objects.filter(
                order_id=order['id'],
                product__vendor=vendor
            ).count()
            order['items_count'] = items_count
            results.append(order)

        return Response({
            'count': len(results),
            'results': results
        })