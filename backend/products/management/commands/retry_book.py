import time

import requests
from django.core.management.base import BaseCommand
from products.models import Product

OPENLIBRARY_SEARCH_URL = "https://openlibrary.org/search.json"
COVER_URL_TEMPLATE = "https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"


def fetch_cover_with_retry(title, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            r = requests.get(
                OPENLIBRARY_SEARCH_URL,
                params={"title": title, "limit": 1, "fields": "title,cover_i"},
                timeout=25,
            )
            if r.status_code == 200:
                docs = r.json().get("docs", [])
                if docs and docs[0].get("cover_i"):
                    return docs[0]["cover_i"]
                return None
        except requests.exceptions.RequestException:
            if attempt < max_attempts - 1:
                time.sleep(4 * (attempt + 1))
                continue
    return "FAILED"


class Command(BaseCommand):
    help = "Retry fetching book covers for items still missing one, with better retry logic"

    def handle(self, *args, **options):
        products = Product.objects.filter(cover_image__isnull=True) | Product.objects.filter(cover_image="")
        products = products.distinct()
        total = products.count()
        fixed = 0
        still_missing = []

        self.stdout.write(self.style.SUCCESS(f"\nRetrying {total} books still missing covers...\n"))

        for i, product in enumerate(products, 1):
            search_title = product.name.replace("⭐ ", "").strip()
            cover_id = fetch_cover_with_retry(search_title)

            if cover_id == "FAILED" or cover_id is None:
                still_missing.append(search_title)
                self.stdout.write(self.style.WARNING(f"  [{i}/{total}] No cover: {search_title[:50]}"))
            else:
                product.cover_image = COVER_URL_TEMPLATE.format(cover_id=cover_id)
                product.save()
                fixed += 1
                self.stdout.write(f"  [{i}/{total}] FIXED: {search_title[:50]}")

            time.sleep(0.4)

        self.stdout.write(self.style.SUCCESS(f"\n{'='*60}"))
        self.stdout.write(self.style.SUCCESS(f"Fixed this run: {fixed}"))
        self.stdout.write(self.style.WARNING(f"Still missing (fine, uses fallback): {len(still_missing)}"))
