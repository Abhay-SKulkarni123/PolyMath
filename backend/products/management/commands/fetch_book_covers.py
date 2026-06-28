"""
STEP 2 - ADD THIS as backend/products/management/commands/fetch_book_covers.py

Run this AFTER adding the cover_image field and migrating.

For every Product with no cover_image, searches Open Library by title
(text search, not a guessed ID - Open Library's search is free, no API key,
and a completely different domain/service than TMDB so none of the SSL
issues from this session should apply here).

If a real cover_i (cover ID) comes back, builds the direct image URL and
SAVES it properly this time - unlike the original script, this one actually
persists the value instead of discarding it.

Open Library cover URL pattern (no API key needed):
    https://covers.openlibrary.org/b/id/{cover_id}-L.jpg

Run:
    cd backend
    python manage.py fetch_book_covers
"""
import time
import requests
from django.core.management.base import BaseCommand
from products.models import Product

OPENLIBRARY_SEARCH_URL = "https://openlibrary.org/search.json"
COVER_URL_TEMPLATE = "https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"


class Command(BaseCommand):
    help = "Fetch and properly SAVE real book cover URLs from Open Library"

    def handle(self, *args, **options):
        products = Product.objects.filter(cover_image__isnull=True) | Product.objects.filter(cover_image="")
        products = products.distinct()
        total = products.count()
        fixed = 0
        no_cover_found = []

        self.stdout.write(self.style.SUCCESS(f"\nFetching covers for {total} books with no cover_image...\n"))

        for i, product in enumerate(products, 1):
            # Strip the "⭐ " prefix some featured books have, for a cleaner search query
            search_title = product.name.replace("⭐ ", "").strip()

            try:
                r = requests.get(
                    OPENLIBRARY_SEARCH_URL,
                    params={"title": search_title, "limit": 1, "fields": "title,cover_i"},
                    timeout=15,
                )
                if r.status_code == 200:
                    docs = r.json().get("docs", [])
                    if docs and docs[0].get("cover_i"):
                        cover_id = docs[0]["cover_i"]
                        cover_url = COVER_URL_TEMPLATE.format(cover_id=cover_id)

                        product.cover_image = cover_url
                        product.save()
                        fixed += 1
                        self.stdout.write(f"  [{i}/{total}] FIXED: {search_title[:50]}")
                    else:
                        no_cover_found.append(search_title)
                        self.stdout.write(self.style.WARNING(f"  [{i}/{total}] No cover available: {search_title[:50]}"))
                else:
                    no_cover_found.append(search_title)
                    self.stdout.write(self.style.WARNING(f"  [{i}/{total}] API error {r.status_code}: {search_title[:50]}"))
            except Exception as e:
                no_cover_found.append(search_title)
                self.stdout.write(self.style.WARNING(f"  [{i}/{total}] Error: {search_title[:50]} - {e}"))

            time.sleep(0.2)

        self.stdout.write(self.style.SUCCESS(f"\n{'='*60}"))
        self.stdout.write(self.style.SUCCESS(f"DONE"))
        self.stdout.write(self.style.SUCCESS(f"{'='*60}"))
        self.stdout.write(self.style.SUCCESS(f"Covers fixed:    {fixed}"))
        self.stdout.write(self.style.WARNING(f"No cover found:  {len(no_cover_found)} (will use gradient fallback - that's fine)"))