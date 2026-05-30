import os
import requests
import urllib3
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FIELD_SEARCH_TERMS = {
    'science-nature': 'science nature documentary',
    'technology-computing': 'technology artificial intelligence',
    'literature-stories': 'books writers literature',
    'music-sound': 'music musicians',
    'visual-arts-design': 'art painting design',
    'culinary-arts': 'cooking chef food',
    'history-philosophy': 'history philosophy',
    'health-performance': 'fitness sports health',
    'film-cinema': 'filmmaking cinema directors',
    'languages-culture': 'culture travel language',
    'space-cosmos': 'space',
    'psychology-mind': 'psychology mind brain',
}


class MoviesByFieldView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        field_slug = request.query_params.get('field')

        if not field_slug:
            return Response(
                {'error': 'field parameter is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        search_term = FIELD_SEARCH_TERMS.get(field_slug)

        if not search_term:
            return Response(
                {'error': 'Unknown knowledge field.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        api_key = os.getenv('TMDB_API_KEY')

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }

        try:
            session = requests.Session()
            session.verify = False
            adapter = requests.adapters.HTTPAdapter()
            session.mount('https://', adapter)

            response = session.get(
                'https://api.themoviedb.org/3/search/movie',
                headers=headers,
                params={
                    'query': search_term,
                    'include_adult': False,
                    'language': 'en-US',
                    'page': 1,
                },
                timeout=15
            )
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print(f"TMDB Error: {e}")
            return Response(
                {'error': 'Failed to fetch movies from TMDB.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        data = response.json()
        movies = []

        for movie in data.get('results', [])[:8]:
            poster = movie.get('poster_path')
            if not movie.get('title') or not movie.get('overview'):
                continue
            movies.append({
                'id': movie['id'],
                'title': movie['title'],
                'overview': movie['overview'],
                'release_date': movie.get('release_date', ''),
                'rating': round(movie.get('vote_average', 0), 1),
                'poster': f'https://image.tmdb.org/t/p/w500{poster}' if poster else None,
                'tmdb_url': f'https://www.themoviedb.org/movie/{movie["id"]}',
            })

        return Response({
            'field': field_slug,
            'total_results': data.get('total_results', 0),
            'movies': movies
        })