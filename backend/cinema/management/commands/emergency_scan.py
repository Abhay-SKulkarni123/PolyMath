import time
import requests
from django.core.management.base import BaseCommand
from cinema.models import Movie

API_KEY = "be071106a7d116eb087c1512c6ddfc01"
BASE_URL = "https://api.themoviedb.org/3"


class Command(BaseCommand):
    help = "URGENT: scan and remove any adult-flagged content from movie images"

    def handle(self, *args, **options):
        movies = Movie.objects.all()
        total = movies.count()
        wiped = []
        checked = 0
        errors = []

        self.stdout.write(self.style.ERROR(f"\nSCANNING {total} MOVIES FOR ADULT CONTENT FLAGS...\n"))

        for i, movie in enumerate(movies, 1):
            media_type = "tv" if movie.type == "series" else "movie"

            try:
                r = requests.get(
                    f"{BASE_URL}/{media_type}/{movie.tmdb_id}",
                    params={"api_key": API_KEY},
                    timeout=20,
                )
                if r.status_code == 200:
                    data = r.json()
                    checked += 1
                    if data.get("adult") is True:
                        movie.poster_path = ""
                        movie.backdrop_path = ""
                        movie.save()
                        wiped.append((movie.id, movie.title, movie.tmdb_id))
                        self.stdout.write(self.style.ERROR(f"  WIPED (adult flagged): {movie.title} (id={movie.id}, tmdb_id={movie.tmdb_id})"))
            except Exception as e:
                errors.append(movie.title)

            if i % 30 == 0:
                self.stdout.write(f"  ... checked {i}/{total} ...")

            time.sleep(0.1)

        self.stdout.write(self.style.SUCCESS(f"\n{'='*60}"))
        self.stdout.write(self.style.SUCCESS(f"SCAN COMPLETE"))
        self.stdout.write(self.style.SUCCESS(f"{'='*60}"))
        self.stdout.write(self.style.SUCCESS(f"Checked: {checked}/{total}"))
        self.stdout.write(self.style.ERROR(f"Wiped (adult content): {len(wiped)}"))
        if wiped:
            self.stdout.write(self.style.ERROR("\n--- WIPED MOVIES (these now show safe fallback) ---"))
            for mid, title, tmdb_id in wiped:
                self.stdout.write(f"  id={mid}, title='{title}', tmdb_id={tmdb_id}")
        if errors:
            self.stdout.write(self.style.WARNING(f"\nCouldn't check (network errors, re-run to retry): {len(errors)}"))