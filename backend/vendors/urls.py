from django.urls import path
from .views import VendorStatsView, VendorProductsView, VendorOrdersView

urlpatterns = [
    path('stats/', VendorStatsView.as_view(), name='vendor-stats'),
    path('products/', VendorProductsView.as_view(), name='vendor-products'),
    path('orders/', VendorOrdersView.as_view(), name='vendor-orders'),
]