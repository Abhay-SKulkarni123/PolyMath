from django.urls import path
from .views import (
    CollectionListView,
    CollectionDetailView,
    CollectionMoviesView,
    MovieDetailView,
    FeaturedMoviesView,
)

urlpatterns = [
    path('collections/', CollectionListView.as_view(), name='collection-list'),
    path('collections/<slug:slug>/', CollectionDetailView.as_view(), name='collection-detail'),
    path('collections/<slug:slug>/movies/', CollectionMoviesView.as_view(), name='collection-movies'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie-detail'),
    path('movies/featured/', FeaturedMoviesView.as_view(), name='featured-movies'),
]