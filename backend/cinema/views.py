import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Collection, Movie
from .serializers import CollectionSerializer, CollectionListSerializer, MovieSerializer

logger = logging.getLogger()

class CollectionListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            category = request.query_params.get('category', None)
            collections = Collection.objects.filter(is_active=True)
            if category:
                collections = collections.filter(category=category)
            serializer = CollectionListSerializer(collections, many=True)
            return Response({'error': False, 'results': serializer.data})
        except Exception as e:
            logger.error(f"CollectionList error: {str(e)}")
            return Response({'error': True, 'message': 'Failed to fetch collections'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CollectionDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        try:
            collection = Collection.objects.get(slug=slug, is_active=True)
            serializer = CollectionSerializer(collection)
            return Response({'error': False, 'data': serializer.data})
        except Collection.DoesNotExist:
            return Response({'error': True, 'message': 'Collection not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"CollectionDetail error: {str(e)}")
            return Response({'error': True, 'message': 'Failed to fetch collection'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CollectionMoviesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        try:
            collection = Collection.objects.get(slug=slug, is_active=True)
            movies = collection.movies.all().order_by('-vote_average', '-popularity')
            serializer = MovieSerializer(movies, many=True)
            return Response({'error': False, 'results': serializer.data, 'collection': collection.name})
        except Collection.DoesNotExist:
            return Response({'error': True, 'message': 'Collection not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"CollectionMovies error: {str(e)}")
            return Response({'error': True, 'message': 'Failed to fetch movies'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MovieDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            movie = Movie.objects.get(id=pk)
            serializer = MovieSerializer(movie)
            related = Movie.objects.filter(collection=movie.collection).exclude(id=pk).order_by('-vote_average')[:10]
            related_serializer = MovieSerializer(related, many=True)
            return Response({
                'error': False,
                'data': serializer.data,
                'related': related_serializer.data,
                'collection': {
                    'name': movie.collection.name,
                    'slug': movie.collection.slug,
                    'icon': movie.collection.icon,
                }
            })
        except Movie.DoesNotExist:
            return Response({'error': True, 'message': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"MovieDetail error: {str(e)}")
            return Response({'error': True, 'message': 'Failed to fetch movie'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FeaturedMoviesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            movies = Movie.objects.filter(is_featured=True).order_by('-vote_average')[:20]
            serializer = MovieSerializer(movies, many=True)
            return Response({'error': False, 'results': serializer.data})
        except Exception as e:
            logger.error(f"FeaturedMovies error: {str(e)}")
            return Response({'error': True, 'message': 'Failed to fetch featured movies'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)