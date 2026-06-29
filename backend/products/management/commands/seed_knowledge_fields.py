"""
ADD THIS as backend/products/management/commands/seed_knowledge_fields.py

Creates the 12 KnowledgeField records that seed_books expects to already
exist (same root cause as the vendor issue - this data existed on the
old local DB but was never created on the fresh Railway database).

Run BEFORE seed_books:
    railway run python manage.py seed_knowledge_fields

Then:
    railway run python manage.py seed_books
"""
from django.core.management.base import BaseCommand
from products.models import KnowledgeField

FIELDS = [
    ("Science & Nature", "science-nature", "🔬"),
    ("Technology & Computing", "technology-computing", "💻"),
    ("Literature & Stories", "literature-stories", "📖"),
    ("Music & Sound", "music-sound", "🎵"),
    ("Visual Arts & Design", "visual-arts-design", "🎨"),
    ("Culinary Arts", "culinary-arts", "🍳"),
    ("History & Philosophy", "history-philosophy", "🏛️"),
    ("Health & Performance", "health-performance", "💪"),
    ("Film & Cinema", "film-cinema", "🎬"),
    ("Languages & Culture", "languages-culture", "🌍"),
    ("Space & Cosmos", "space-cosmos", "🚀"),
    ("Psychology & Mind", "psychology-mind", "🧠"),
]


class Command(BaseCommand):
    help = "Seed the 12 KnowledgeField records required by seed_books"

    def handle(self, *args, **options):
        created = 0
        for name, slug, icon in FIELDS:
            field, was_created = KnowledgeField.objects.get_or_create(
                slug=slug,
                defaults={"name": name, "icon": icon},
            )
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"Created: {name} ({slug})"))
            else:
                self.stdout.write(f"Already exists: {name} ({slug})")

        self.stdout.write(self.style.SUCCESS(f"\nDone. Created {created} new fields, {len(FIELDS) - created} already existed."))
        self.stdout.write(self.style.SUCCESS("Now run: python manage.py seed_books"))