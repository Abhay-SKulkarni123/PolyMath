import logging
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Product, KnowledgeField
from .serializers import ProductSerializer, KnowledgeFieldSerializer

logger = logging.getLogger()

class KnowledgeFieldListCreateView(generics.ListCreateAPIView):
    queryset = KnowledgeField.objects.all()
    serializer_class = KnowledgeFieldSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"KnowledgeField fetch error: {str(e)}")
            return Response(
                {'error': True, 'message': 'Failed to fetch knowledge fields'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        try:
            queryset = Product.objects.filter(is_active=True).select_related('vendor').prefetch_related('knowledge_fields')
            
            search = self.request.query_params.get('search', '').strip()
            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search) |
                    Q(description__icontains=search)
                )
            
            field_slug = self.request.query_params.get('field', '').strip()
            if field_slug:
                queryset = queryset.filter(knowledge_fields__slug=field_slug)
            
            product_type = self.request.query_params.get('type', '').strip()
            if product_type in ['physical', 'digital', 'experience']:
                queryset = queryset.filter(type=product_type)
            
            return queryset.distinct().order_by('-created_at')
        
        except Exception as e:
            logger.error(f"ProductList queryset error: {str(e)}")
            return Product.objects.filter(is_active=True)

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"ProductList fetch error: {str(e)}")
            return Response(
                {'error': True, 'message': 'Failed to fetch products'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Product.DoesNotExist:
            logger.warning(f"Product not found: {kwargs.get('pk')}")
            return Response(
                {'error': True, 'message': 'Product not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"ProductDetail fetch error: {str(e)}")
            return Response(
                {'error': True, 'message': 'Failed to fetch product'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                logger.warning(f"Product creation validation failed: {serializer.errors}")
                return Response(
                    {'error': True, 'message': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            self.perform_create(serializer)
            logger.info(f"Product created by {request.user.email}")
            
            return Response(
                {'error': False, 'message': 'Product created', 'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.error(f"Product creation error: {str(e)}")
            return Response(
                {'error': True, 'message': 'Failed to create product'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user.vendorprofile)