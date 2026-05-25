from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
import uuid
from .models import Order, OrderItem
from .serializers import OrderSerializer, CheckoutSerializer
from cart.models import Cart
from django.http import FileResponse
from django.utils import timezone
from products.models import Product


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Cart is empty.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_items = cart.items.select_related('product').all()

        if not cart_items.exists():
            return Response(
                {'error': 'Cart is empty.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate stock only for physical and experience products
        for cart_item in cart_items:
            product = cart_item.product
            if product.type in ['physical', 'experience']:
                if product.stock < cart_item.quantity:
                    return Response(
                        {
                            'error': f'Insufficient stock for {product.name}. '
                                     f'Available: {product.stock}'
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

        # Calculate total
        total_price = sum(
            item.product.price * item.quantity
            for item in cart_items
        )

        # Create order
        order = Order.objects.create(
            user=request.user,
            shipping_address=serializer.validated_data['shipping_address'],
            total_price=total_price,
            status='pending'
        )

        # Create order items
        for cart_item in cart_items:
            product = cart_item.product

            # Generate download token for digital products
            download_token = None
            if product.is_digital:
                download_token = str(uuid.uuid4())

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=cart_item.quantity,
                price=product.price,
                download_token=download_token
            )

            # Reduce stock only for physical and experience products
            if product.type in ['physical', 'experience']:
                product.stock -= cart_item.quantity
                product.save()

        # Clear cart
        cart.items.all().delete()

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).prefetch_related('items__product')

class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).prefetch_related('items__product')
    
class DownloadProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, token):
        try:
            order_item = OrderItem.objects.select_related(
                'product', 'order'
            ).get(
                download_token=token,
                order__user=request.user
            )
        except OrderItem.DoesNotExist:
            return Response(
                {'error': 'Invalid or expired download link.'},
                status=status.HTTP_404_NOT_FOUND
            )

        product = order_item.product

        if not product.file:
            return Response(
                {'error': 'No file available for this product.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Mark as downloaded
        order_item.downloaded_at = timezone.now()
        order_item.save()

        # Serve the file
        response = FileResponse(
            product.file.open('rb'),
            as_attachment=True,
            filename=product.file.name.split('/')[-1]
        )
        return response