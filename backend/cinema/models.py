from django.db import models


class Collection(models.Model):
    CATEGORY_CHOICES = [
        ("superhero", "Superhero Universe"),
        ("indian_epic", "Indian Epics"),
        ("fantasy", "Fantasy & Sci-Fi"),
        ("franchise", "Iconic Franchise"),
        ("series", "Web Series"),
        ("anime", "Anime"),
        ("indian_cinema", "Indian Cinema"),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, default="🎬")
    banner_path = models.CharField(max_length=500, blank=True)
    poster_path = models.CharField(max_length=500, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="franchise")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "name"]

    @property
    def banner_url(self):
        if self.banner_path:
            return f"https://image.tmdb.org/t/p/original{self.banner_path}"
        return None

    @property
    def poster_url(self):
        if self.poster_path:
            return f"https://image.tmdb.org/t/p/w500{self.poster_path}"
        return None

    def __str__(self):
        return self.name


class Movie(models.Model):
    TYPE_CHOICES = [
        ("movie", "Movie"),
        ("series", "Web Series"),
        ("anime", "Anime"),
        ("documentary", "Documentary"),
    ]

    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="movies")
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=300)
    overview = models.TextField(blank=True)
    poster_path = models.CharField(max_length=500, blank=True)
    backdrop_path = models.CharField(max_length=500, blank=True)
    release_date = models.CharField(max_length=20, blank=True)
    vote_average = models.FloatField(default=0)
    vote_count = models.IntegerField(default=0)
    popularity = models.FloatField(default=0)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="movie")
    watch_url = models.URLField(max_length=500, blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-vote_average", "-popularity"]

    def __str__(self):
        return self.title

    @property
    def poster_url(self):
        if self.poster_path:
            return f"https://image.tmdb.org/t/p/w500{self.poster_path}"
        return None

    @property
    def backdrop_url(self):
        if self.backdrop_path:
            return f"https://image.tmdb.org/t/p/original{self.backdrop_path}"
        return None
