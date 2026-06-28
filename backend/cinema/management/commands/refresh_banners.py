from django.core.management.base import BaseCommand
from cinema.models import Collection


class Command(BaseCommand):
    help = "Refresh ALL collection banners/posters from their best movie's CURRENT working images"

    def handle(self, *args, **options):
        collections = Collection.objects.all()
        fixed = 0
        no_movies = []

        for col in collections:
            movies = col.movies.order_by('-vote_average', '-popularity')

            best_backdrop_movie = movies.exclude(backdrop_path='').first()
            best_poster_movie = movies.exclude(poster_path='').first()

            changed = False
            if best_backdrop_movie:
                col.banner_path = best_backdrop_movie.backdrop_path
                changed = True
            if best_poster_movie:
                col.poster_path = best_poster_movie.poster_path
                changed = True

            if changed:
                col.save()
                fixed += 1
                self.stdout.write(self.style.SUCCESS(f"REFRESHED: {col.name}"))
            else:
                no_movies.append(col.name)
                self.stdout.write(self.style.WARNING(f"No movies with images: {col.name}"))

        self.stdout.write(self.style.SUCCESS(f"\n{'='*50}"))
        self.stdout.write(self.style.SUCCESS(f"Refreshed: {fixed}/{collections.count()}"))
        if no_movies:
            self.stdout.write(self.style.WARNING(f"Skipped (no movies with images): {no_movies}"))