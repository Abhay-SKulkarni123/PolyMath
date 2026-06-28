import time
import requests
from django.core.management.base import BaseCommand
from cinema.models import Collection

BROKEN_COLLECTION_SLUGS = [
    "dc-universe", "x-men-universe", "star-wars-saga", "lord-of-the-rings",
    "monsterverse", "jurassic-park-universe", "john-wick-universe",
    "mission-impossible", "marvel-disney-series", "star-wars-series",
]


def check_image_loads(url, max_attempts=2):
    for attempt in range(max_attempts):
        try:
            r = requests.head(url, timeout=10, allow_redirects=True)
            return r.status_code == 200
        except requests.exceptions.RequestException:
            if attempt < max_attempts - 1:
                time.sleep(2)
                continue
    return False


class Command(BaseCommand):
    help = "Find a working backdrop for each of the 10 confirmed-broken collection banners"

    def handle(self, *args, **options):
        fixed = 0
        still_broken = []

        for slug in BROKEN_COLLECTION_SLUGS:
            col = Collection.objects.filter(slug=slug).first()
            if not col:
                self.stdout.write(self.style.WARNING(f"Not found: {slug}"))
                continue

            movies = col.movies.exclude(backdrop_path='').order_by('-vote_average', '-popularity')
            found = False

            for movie in movies:
                url = f"https://image.tmdb.org/t/p/w780{movie.backdrop_path}"
                if check_image_loads(url):
                    col.banner_path = movie.backdrop_path
                    col.save()
                    self.stdout.write(self.style.SUCCESS(f"FIXED: {col.name} -> using '{movie.title}'s backdrop"))
                    fixed += 1
                    found = True
                    break
                time.sleep(0.1)

            if not found:
                still_broken.append(col.name)
                self.stdout.write(self.style.ERROR(f"NO WORKING BACKDROP FOUND in any movie: {col.name}"))

        self.stdout.write(self.style.SUCCESS(f"\n{'='*50}"))
        self.stdout.write(self.style.SUCCESS(f"Fixed: {fixed}/{len(BROKEN_COLLECTION_SLUGS)}"))
        if still_broken:
            self.stdout.write(self.style.ERROR(f"Still broken (no movie has a working backdrop): {still_broken}"))