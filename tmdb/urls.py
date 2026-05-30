from django.urls import path
from .views import MoviesByFieldView

urlpatterns = [
    path('movies/', MoviesByFieldView.as_view(), name='movies-by-field'),
]