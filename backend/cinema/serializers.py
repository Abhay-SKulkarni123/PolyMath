from rest_framework import serializers

from .models import Collection, Movie


class MovieSerializer(serializers.ModelSerializer):
    poster_url = serializers.ReadOnlyField()
    backdrop_url = serializers.ReadOnlyField()

    class Meta:
        model = Movie
        fields = [
            "id",
            "tmdb_id",
            "title",
            "overview",
            "poster_path",
            "backdrop_path",
            "poster_url",
            "backdrop_url",
            "release_date",
            "vote_average",
            "vote_count",
            "popularity",
            "type",
            "watch_url",
            "is_featured",
            "order",
        ]


class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, read_only=True)
    movie_count = serializers.SerializerMethodField()
    top_movies = serializers.SerializerMethodField()
    banner_url = serializers.ReadOnlyField()
    poster_url = serializers.ReadOnlyField()

    class Meta:
        model = Collection
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "icon",
            "banner_path",
            "poster_path",
            "banner_url",
            "poster_url",
            "category",
            "order",
            "movie_count",
            "movies",
            "top_movies",
        ]

    def get_movie_count(self, obj):
        return obj.movies.count()

    def get_top_movies(self, obj):
        top = obj.movies.order_by("-vote_average", "-popularity")[:10]
        return MovieSerializer(top, many=True).data


class CollectionListSerializer(serializers.ModelSerializer):
    movie_count = serializers.SerializerMethodField()
    top_movies = serializers.SerializerMethodField()
    banner_url = serializers.ReadOnlyField()
    poster_url = serializers.ReadOnlyField()

    class Meta:
        model = Collection
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "icon",
            "banner_path",
            "poster_path",
            "banner_url",
            "poster_url",
            "category",
            "order",
            "movie_count",
            "top_movies",
        ]

    def get_movie_count(self, obj):
        return obj.movies.count()

    def get_top_movies(self, obj):
        top = obj.movies.order_by("-vote_average", "-popularity")[:6]
        return MovieSerializer(top, many=True).data
