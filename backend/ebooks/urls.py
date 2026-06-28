from django.urls import path
from .views import FreeEbooksView

urlpatterns = [
    path('free/', FreeEbooksView.as_view(), name='free-ebooks'),
]