import time
import requests
from django.core.management.base import BaseCommand
from cinema.models import Movie


def check_image_loads(url, max_attempts=2):
    """HEAD request - much lighter than downloading the full image,
    just confirms the URL resolves with a 200."""
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
    help = "Comprehensive audit: empty poster_path AND broken/unreachable poster URLs"

    def handle(self, *args, **options):
        movies = Movie.objects.all().order_by('id')
        total = movies.count()

        empty_path = []
        broken_url = []
        working = 0

        self.stdout.write(self.style.SUCCESS(f"\nAuditing {total} movies (this checks live URLs, will take a few minutes)...\n"))

        for i, m in enumerate(movies, 1):
            if not m.poster_path:
                empty_path.append((m.id, m.title, m.tmdb_id))
                self.stdout.write(self.style.WARNING(f"  [{i}/{total}] EMPTY PATH: {m.title} (id={m.id})"))
                continue

            url = f"https://image.tmdb.org/t/p/w300{m.poster_path}"
            if check_image_loads(url):
                working += 1
            else:
                broken_url.append((m.id, m.title, m.tmdb_id, m.poster_path))
                self.stdout.write(self.style.ERROR(f"  [{i}/{total}] BROKEN URL: {m.title} (id={m.id}, path={m.poster_path})"))

            time.sleep(0.05)

        self.stdout.write(self.style.SUCCESS(f"\n{'='*60}"))
        self.stdout.write(self.style.SUCCESS(f"AUDIT COMPLETE"))
        self.stdout.write(self.style.SUCCESS(f"{'='*60}"))
        self.stdout.write(self.style.SUCCESS(f"Working posters:    {working}"))
        self.stdout.write(self.style.WARNING(f"Empty poster_path:   {len(empty_path)}"))
        self.stdout.write(self.style.ERROR(f"Broken/unreachable:  {len(broken_url)}"))

        if empty_path:
            self.stdout.write(self.style.WARNING("\n--- EMPTY PATH (id, title, tmdb_id) ---"))
            for row in empty_path:
                self.stdout.write(f"{row[0]}\t{row[1]}\t{row[2]}")

        if broken_url:
            self.stdout.write(self.style.ERROR("\n--- BROKEN URL (id, title, tmdb_id, path) ---"))
            for row in broken_url:
                self.stdout.write(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}")

        self.stdout.write(self.style.SUCCESS(f"\nTotal needing fixes: {len(empty_path) + len(broken_url)}"))