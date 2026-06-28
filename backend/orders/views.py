import logging
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Order, OrderItem
from .serializers import OrderSerializer, CheckoutSerializer
from cart.models import Cart
from products.models import Product
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger('api')

class CheckoutView(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            serializer = CheckoutSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {'error': True, 'message': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            cart = Cart.objects.get(user=request.user)
            if not cart.items.exists():
                return Response(
                    {'error': True, 'message': 'Cart is empty'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            order = Order.objects.create(
                user=request.user,
                shipping_address=serializer.validated_data['shipping_address'],
                total_price=cart.total_price,
                status='pending'
            )
            
            for item in cart.items.all():
                product = item.product
                
                if not product.is_digital and product.stock < item.quantity:
                    raise Exception('Insufficient stock')
                
                if not product.is_digital:
                    product.stock -= item.quantity
                    product.save()
                
                download_token = None
                if product.is_digital:
                    download_token = str(uuid.uuid4())
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item.quantity,
                    price=product.price,
                    download_token=download_token
                )
            
            cart.items.all().delete()
            logger.info(f"Order created: {order.id} by {request.user.email}")
            
            return Response(
                {'error': False, 'message': 'Order placed', 'id': order.id, 'data': OrderSerializer(order).data},
                status=status.HTTP_201_CREATED
            )
        
        except Exception as e:
            logger.error(f"Checkout error: {str(e)}")
            return Response(
                {'error': True, 'message': 'Failed to place order'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class OrderListView(APIView):
    def get(self, request):
        try:
            orders = Order.objects.filter(user=request.user).order_by('-created_at')
            serializer = OrderSerializer(orders, many=True)
            return Response({'error': False, 'results': serializer.data})
        except Exception as e:
            logger.error(f"OrderList error: {str(e)}")
            return Response(
                {'error': True, 'message': 'Failed to fetch orders'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class OrderDetailView(APIView):
    def get(self, request, pk):
        try:
            order = Order.objects.get(id=pk, user=request.user)
            serializer = OrderSerializer(order)
            return Response({'error': False, 'data': serializer.data})
        except Order.DoesNotExist:
            return Response(
                {'error': True, 'message': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"OrderDetail error: {str(e)}")
            return Response(
                {'error': True, 'message': 'Failed to fetch order'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DownloadProductView(APIView):
    def get(self, request, token):
        try:
            order_item = OrderItem.objects.get(download_token=token)
            
            if order_item.order.user != request.user:
                return Response(
                    {'error': True, 'message': 'Unauthorized'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            if not order_item.product.file:
                return Response(
                    {'error': True, 'message': 'File not available'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            from django.http import FileResponse
            from django.utils import timezone
            
            order_item.downloaded_at = timezone.now()
            order_item.save()
            
            logger.info(f"Product downloaded: {order_item.product.id}")
            
            return FileResponse(order_item.product.file.open('rb'))
        
        except OrderItem.DoesNotExist:
            return Response(
                {'error': True, 'message': 'Download link invalid'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Download error: {str(e)}")
            return Response(
                {'error': True, 'message': 'Failed to download'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        




class OrderCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            logger.warning(f"Cancel attempted on missing/foreign order: {pk} by {request.user.email}")
            return Response(
                {'error': True, 'message': 'Order not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if order.status == 'completed':
            return Response(
                {'error': True, 'message': 'Completed orders cannot be cancelled.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if order.status == 'cancelled':
            return Response(
                {'error': True, 'message': 'Order is already cancelled.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = 'cancelled'
        order.save()
        logger.info(f"Order #{order.id} cancelled by {request.user.email}")

        return Response(
            {'error': False, 'message': 'Order cancelled successfully.'},
            status=status.HTTP_200_OK
        )