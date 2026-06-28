from django.urls import path
from .views import CheckoutView, OrderListView, OrderDetailView, DownloadProductView, OrderCancelView
urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('', OrderListView.as_view(), name='order-list'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('download/<uuid:token>/', DownloadProductView.as_view(), name='download'),
    path('<int:pk>/cancel/', OrderCancelView.as_view(), name='order-cancel'),
]