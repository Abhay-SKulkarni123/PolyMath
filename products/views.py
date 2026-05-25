from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from .models import KnowledgeField, Product
from .serializers import KnowledgeFieldSerializer, ProductSerializer
from core.permissions import IsVendor, IsAdmin, IsOwnerOrAdmin


class KnowledgeFieldListCreateView(generics.ListCreateAPIView):
    queryset = KnowledgeField.objects.all()
    serializer_class = KnowledgeFieldSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdmin()]


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'vendor__store_name']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Product.objects.filter(
            is_active=True
        ).select_related('vendor').prefetch_related('knowledge_fields')

        knowledge_field = self.request.query_params.get('field')
        product_type = self.request.query_params.get('type')

        if knowledge_field:
            queryset = queryset.filter(
                knowledge_fields__slug=knowledge_field
            )

        if product_type:
            queryset = queryset.filter(type=product_type)

        return queryset


class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsVendor]

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user.vendor_profile)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsOwnerOrAdmin()]