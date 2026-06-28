from django.core.management.base import BaseCommand
from cinema.models import Collection


class Command(BaseCommand):
    help = "Backfill empty collection banner_path/poster_path from their best movie"

    def handle(self, *args, **options):
        collections = Collection.objects.all()
        fixed = 0
        already_ok = 0
        no_movies_with_images = []

        for col in collections:
            needs_banner = not col.banner_path
            needs_poster = not col.poster_path

            if not needs_banner and not needs_poster:
                already_ok += 1
                continue

            movies = col.movies.order_by('-vote_average', '-popularity')

            if needs_banner:
                best_with_backdrop = movies.exclude(backdrop_path='').first()
                if best_with_backdrop:
                    col.banner_path = best_with_backdrop.backdrop_path

            if needs_poster:
                best_with_poster = movies.exclude(poster_path='').first()
                if best_with_poster:
                    col.poster_path = best_with_poster.poster_path

            if col.banner_path or col.poster_path:
                col.save()
                fixed += 1
                self.stdout.write(self.style.SUCCESS(f"FIXED: {col.name} (banner={bool(col.banner_path)}, poster={bool(col.poster_path)})"))
            else:
                no_movies_with_images.append(col.name)
                self.stdout.write(self.style.WARNING(f"NO IMAGES AVAILABLE: {col.name} (0 movies have images)"))

        self.stdout.write(self.style.SUCCESS(f"\n{'='*50}"))
        self.stdout.write(self.style.SUCCESS(f"Fixed: {fixed}"))
        self.stdout.write(self.style.SUCCESS(f"Already OK: {already_ok}"))
        if no_movies_with_images:
            self.stdout.write(self.style.WARNING(f"Still empty (no movies have images): {no_movies_with_images}"))