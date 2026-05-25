from django.urls import path
from .views import (
    KnowledgeFieldListCreateView,
    ProductListView,
    ProductCreateView,
    ProductDetailView,
)

urlpatterns = [
    path('fields/', KnowledgeFieldListCreateView.as_view(), name='knowledge-field-list'),
    path('', ProductListView.as_view(), name='product-list'),
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]
