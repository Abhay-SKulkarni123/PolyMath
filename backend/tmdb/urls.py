from django.urls import path
from .views import TMDBMoviesView

urlpatterns = [
    path('movies/', TMDBMoviesView.as_view(), name='tmdb-movies'),
]