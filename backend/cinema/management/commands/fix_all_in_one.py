import time
import requests
from django.core.management.base import BaseCommand
from cinema.models import Movie, Collection

API_KEY = "be071106a7d116eb087c1512c6ddfc01"
BASE_URL = "https://api.themoviedb.org/3"


def fetch_with_retry(tmdb_id, media_type, max_attempts=3):
    """Direct TMDB lookup with adult-content safety check baked in -
    any response flagged adult=True is treated as unusable, same as
    a 404, so the caller never receives or saves that data."""
    for attempt in range(max_attempts):
        try:
            r = requests.get(
                f"{BASE_URL}/{media_type}/{tmdb_id}",
                params={"api_key": API_KEY},
                timeout=20,
            )
            if r.status_code == 200:
                data = r.json()
                if data.get("adult") is True:
                    return "ADULT_BLOCKED"
                return data
            elif r.status_code == 404:
                return None
        except (requests.exceptions.ConnectionError, requests.exceptions.SSLError, requests.exceptions.Timeout):
            time.sleep(2 * (attempt + 1))
            continue
    return "FAILED"


def check_image_loads(url, max_attempts=2):
    for attempt in range(max_attempts):
        try:
            r = requests.head(url, timeout=10, allow_redirects=True)
            return r.status_code == 200
        except requests.exceptions.RequestException:
            if attempt < max_attempts - 1:
                time.sleep(1)
                continue
    return False


class Command(BaseCommand):
    help = "All-in-one fix: refresh all movie posters, then all collection banners"

    def handle(self, *args, **options):
        # ============================================================
        # PART 1: Refresh all movies
        # ============================================================
        movies = Movie.objects.all()
        total = movies.count()
        movie_fixed = 0
        movie_failed = []

        self.stdout.write(self.style.SUCCESS(f"\n{'='*60}"))
        self.stdout.write(self.style.SUCCESS(f"PART 1: Refreshing {total} movie posters"))
        self.stdout.write(self.style.SUCCESS(f"{'='*60}\n"))

        for i, movie in enumerate(movies, 1):
            media_type = "tv" if movie.type == "series" else "movie"
            data = fetch_with_retry(movie.tmdb_id, media_type)

            if data == "ADULT_BLOCKED":
                self.stdout.write(self.style.ERROR(f"  [{i}/{total}] BLOCKED ADULT CONTENT: {movie.title} - left unchanged"))
                continue

            if data == "FAILED" or data is None:
                movie_failed.append(movie.title)
                if i % 20 == 0:
                    self.stdout.write(f"  [{i}/{total}] ... still working ...")
                continue

            new_poster = data.get("poster_path", "")
            new_backdrop = data.get("backdrop_path", "")

            if new_poster or new_backdrop:
                movie.poster_path = new_poster or movie.poster_path
                movie.backdrop_path = new_backdrop or movie.backdrop_path
                movie.save()
                movie_fixed += 1

            if i % 20 == 0:
                self.stdout.write(f"  [{i}/{total}] processed, {movie_fixed} fixed so far")

            time.sleep(0.1)

        self.stdout.write(self.style.SUCCESS(f"\nPart 1 done: {movie_fixed}/{total} movies refreshed"))
        if movie_failed:
            self.stdout.write(self.style.WARNING(f"Failed/no-data: {len(movie_failed)} titles"))

        # ============================================================
        # PART 2: Refresh all collection banners from verified movies
        # ============================================================
        self.stdout.write(self.style.SUCCESS(f"\n{'='*60}"))
        self.stdout.write(self.style.SUCCESS(f"PART 2: Refreshing collection banners"))
        self.stdout.write(self.style.SUCCESS(f"{'='*60}\n"))

        collections = Collection.objects.all()
        col_fixed = 0
        col_failed = []

        for col in collections:
            col_movies = col.movies.exclude(backdrop_path='').order_by('-vote_average', '-popularity')
            found = False

            for movie in col_movies[:10]:  # only check top 10 to keep this fast
                url = f"https://image.tmdb.org/t/p/w780{movie.backdrop_path}"
                if check_image_loads(url):
                    col.banner_path = movie.backdrop_path
                    found = True
                    break
                time.sleep(0.1)

            col_posters = col.movies.exclude(poster_path='').order_by('-vote_average', '-popularity')
            for movie in col_posters[:10]:
                url = f"https://image.tmdb.org/t/p/w300{movie.poster_path}"
                if check_image_loads(url):
                    col.poster_path = movie.poster_path
                    break
                time.sleep(0.1)

            if found:
                col.save()
                col_fixed += 1
                self.stdout.write(self.style.SUCCESS(f"FIXED: {col.name}"))
            else:
                col_failed.append(col.name)
                self.stdout.write(self.style.WARNING(f"No working backdrop found: {col.name}"))

        self.stdout.write(self.style.SUCCESS(f"\n{'='*60}"))
        self.stdout.write(self.style.SUCCESS(f"ALL DONE"))
        self.stdout.write(self.style.SUCCESS(f"{'='*60}"))
        self.stdout.write(self.style.SUCCESS(f"Movies refreshed: {movie_fixed}/{total}"))
        self.stdout.write(self.style.SUCCESS(f"Collections refreshed: {col_fixed}/{collections.count()}"))
        if col_failed:
            self.stdout.write(self.style.WARNING(f"Collections still broken: {col_failed}"))