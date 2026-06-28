from django.core.management.base import BaseCommand
from cinema.models import Collection


class Command(BaseCommand):
    help = "Print actual banner_path/poster_path for collections to diagnose empty banners"

    def handle(self, *args, **options):
        for col in Collection.objects.all().order_by('order'):
            self.stdout.write(f"{col.name} | slug={col.slug} | banner_path='{col.banner_path}' | poster_path='{col.poster_path}'")