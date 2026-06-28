import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product

logger = logging.getLogger()

class CartView(APIView):
    def get(self, request):
        try:
            cart, created = Cart.objects.get_or_create(user=request.user)
            serializer = CartSerializer(cart)
            return Response({'error': False, 'data': serializer.data})
        except Exception as e:
            logger.error(f"CartView GET error: {str(e)}")
            return Response(
                {'error': True, 'message': 'Failed to fetch cart'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AddToCartView(APIView):
    def post(self, request):
        try:
            product_id = request.data.get('product_id')
            quantity = request.data.get('quantity', 1)
            
            if not product_id:
                return Response(
                    {'error': True, 'message': 'Product ID is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            product = Product.objects.get(id=product_id)
            cart, created = Cart.objects.get_or_create(user=request.user)
            
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            logger.info(f"Product added to cart: {product.id}")
            return Response({'error': False, 'message': 'Added to cart'})
        
        except Product.DoesNotExist:
            return Response(
                {'error': True, 'message': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"AddToCart error: {str(e)}")
            return Response(
                {'error': True, 'message': 'Failed to add to cart'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UpdateCartItemView(APIView):
    def patch(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            quantity = request.data.get('quantity')
            
            if quantity and quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            
            serializer = CartItemSerializer(cart_item)
            return Response({'error': False, 'data': serializer.data})
        
        except CartItem.DoesNotExist:
            return Response(
                {'error': True, 'message': 'Cart item not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"UpdateCartItem error: {str(e)}")
            return Response(
                {'error': True, 'message': 'Failed to update cart'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RemoveCartItemView(APIView):
    def delete(self, request, item_id):
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            cart_item.delete()
            return Response({'error': False, 'message': 'Item removed'})
        
        except CartItem.DoesNotExist:
            return Response(
                {'error': True, 'message': 'Cart item not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"RemoveCartItem error: {str(e)}")
            return Response(
                {'error': True, 'message': 'Failed to remove item'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ClearCartView(APIView):
    def post(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            cart.items.all().delete()
            return Response({'error': False, 'message': 'Cart cleared'})
        except Cart.DoesNotExist:
            return Response({'error': False, 'message': 'Cart cleared'})
        except Exception as e:
            logger.error(f"ClearCart error: {str(e)}")
            return Response(
                {'error': True, 'message': 'Failed to clear cart'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )