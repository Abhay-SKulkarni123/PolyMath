import time
import requests
from django.core.management.base import BaseCommand
from cinema.models import Collection


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
    help = "Verify which collection banner/poster URLs actually load"

    def handle(self, *args, **options):
        collections = Collection.objects.all().order_by('order')
        working = 0
        broken = []

        for col in collections:
            banner_ok = False
            if col.banner_path:
                url = f"https://image.tmdb.org/t/p/w780{col.banner_path}"
                banner_ok = check_image_loads(url)

            if banner_ok:
                working += 1
                self.stdout.write(self.style.SUCCESS(f"OK: {col.name}"))
            else:
                broken.append((col.name, col.banner_path))
                self.stdout.write(self.style.ERROR(f"BROKEN: {col.name} (banner_path={col.banner_path})"))

            time.sleep(0.1)

        self.stdout.write(self.style.SUCCESS(f"\n{'='*50}"))
        self.stdout.write(self.style.SUCCESS(f"Working: {working}/{collections.count()}"))
        if broken:
            self.stdout.write(self.style.ERROR(f"\nBroken collections:"))
            for name, path in broken:
                self.stdout.write(f"  {name}: {path}")