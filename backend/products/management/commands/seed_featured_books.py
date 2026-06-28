import requests
import logging
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from products.models import Product, KnowledgeField
from vendors.models import VendorProfile

logger = logging.getLogger()

OPENLIBRARY_URL = "https://openlibrary.org/search.json"

FEATURED_BOOKS = {
    'technology-computing': {
        'search_terms': ['generative AI', 'artificial intelligence machine learning', 'deep learning neural networks', 'ChatGPT GPT transformers'],
        'description_suffix': '⭐ FEATURED: Cutting-edge AI & Machine Learning content'
    },
    'literature-stories': {
        'search_terms': ['marvel comics superhero', 'comic book collection', 'graphic novels marvel', 'superhero stories'],
        'description_suffix': '⭐ FEATURED: Marvel & Comic Universe'
    },
    'history-philosophy': {
        'search_terms': ['hindu mythology vedas', 'indian history ramayana', 'mahabharata ancient india', 'hindu philosophy bhagavad gita'],
        'description_suffix': '⭐ FEATURED: Hindu Mythology & Ancient Indian History'
    },
}

class Command(BaseCommand):
    help = 'Seed featured premium books in high-demand categories'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('⭐ Starting FEATURED Books Seeding...\n'))

        try:
            vendor = VendorProfile.objects.first()
            if not vendor:
                self.stdout.write(self.style.ERROR('❌ No vendor found.'))
                return

            total_created = 0
            total_skipped = 0

            for field_slug, config in FEATURED_BOOKS.items():
                self.stdout.write(self.style.SUCCESS(f'\n⭐ {field_slug.upper()}'))
                
                try:
                    field = KnowledgeField.objects.get(slug=field_slug)
                    search_terms = config['search_terms']
                    desc_suffix = config['description_suffix']
                    
                    for search_term in search_terms:
                        try:
                            books = self.fetch_books(search_term, limit=10)
                            
                            for book in books:
                                if not book:
                                    continue

                                product_name = book.get('title', 'Unknown')
                                
                                if Product.objects.filter(name=product_name, vendor=vendor).exists():
                                    total_skipped += 1
                                    continue

                                author = ', '.join(book.get('author_name', ['Unknown'])[:2]) if book.get('author_name') else 'Unknown'
                                year = book.get('first_publish_year', 2024)
                                isbn = book.get('isbn', [''])[0] if book.get('isbn') else 'N/A'

                                description = f"⭐ FEATURED PREMIUM COLLECTION\n\nAuthor: {author}\nPublished: {year}\nISBN: {isbn}\n\n{product_name}\n\n{desc_suffix}\n\nThis premium edition provides comprehensive coverage and exclusive insights into this fascinating subject."

                                # Premium pricing for featured books
                                base_prices = {
                                    'technology-computing': 59.99,
                                    'literature-stories': 34.99,
                                    'history-philosophy': 44.99,
                                }
                                base_price = base_prices.get(field_slug, 39.99)
                                price = round(base_price + (hash(product_name) % 15), 2)

                                product = Product.objects.create(
                                    vendor=vendor,
                                    name=f"⭐ {product_name[:140]}",
                                    description=description[:1000],
                                    price=str(price),
                                    stock=0,
                                    type='digital',
                                    is_active=True,
                                )

                                product.knowledge_fields.add(field)

                                # Premium content
                                content = self.create_premium_content(
                                    product_name, author, year, field.name, desc_suffix
                                )
                                filename = f"featured_{product_name[:30].replace(' ', '_')}.txt"
                                product.file.save(filename, ContentFile(content.encode()), save=True)

                                total_created += 1
                                self.stdout.write(f"  ⭐ {product_name[:55]}")

                        except Exception as e:
                            logger.error(f"Error: {str(e)}")
                            continue

                except KnowledgeField.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'⚠ Field not found'))

            self.stdout.write(self.style.SUCCESS(f'\n{"="*60}'))
            self.stdout.write(self.style.SUCCESS(f'⭐ FEATURED SEEDING COMPLETE'))
            self.stdout.write(self.style.SUCCESS(f'{"="*60}'))
            self.stdout.write(self.style.SUCCESS(f'✨ Created: {total_created} featured products'))
            self.stdout.write(self.style.SUCCESS(f'⊘ Skipped: {total_skipped}'))
            self.stdout.write(self.style.SUCCESS(f'{"="*60}\n'))

        except Exception as e:
            logger.error(f"Seeding failed: {str(e)}")
            self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))

    def fetch_books(self, query, limit=10):
        """Fetch books from Open Library"""
        try:
            params = {
                'title': query,
                'limit': limit,
                'fields': 'key,title,author_name,first_publish_year,isbn,cover_i'
            }
            response = requests.get(OPENLIBRARY_URL, params=params, timeout=15)
            return response.json().get('docs', [])
        except Exception as e:
            logger.error(f"API error: {str(e)}")
            return []

    def create_premium_content(self, title, author, year, field, category):
        """Create rich premium content"""
        return f"""
╔══════════════════════════════════════════════════════════════╗
║            ⭐ PREMIUM FEATURED EDITION ⭐                   ║
║                    {title[:45]}
╚══════════════════════════════════════════════════════════════╝

Author: {author}
Published: {year}
Field: {field}
Category: {category}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌟 PREMIUM COLLECTION HIGHLIGHTS

This is part of our FEATURED PREMIUM collection, carefully curated for maximum value and relevance.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 COMPREHENSIVE CONTENT

- In-depth analysis and expert insights
- Practical examples and real-world applications  
- Advanced concepts and cutting-edge developments
- Exclusive perspectives from industry leaders
- Interactive exercises and learning materials
- Extended bibliography and reference materials

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ WHY THIS BOOK?

This premium selection offers:
✓ Expert-authored content
✓ Comprehensive coverage
✓ Practical applications
✓ Advanced insights
✓ Continuing value

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 PERFECT FOR

- Students seeking deep knowledge
- Professionals advancing their expertise
- Enthusiasts exploring new interests
- Researchers needing comprehensive references
- Anyone serious about mastery

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💎 PREMIUM VALUE

Gain access to curated, high-quality content that goes beyond 
the basics. This featured edition represents the finest 
resources in {field}.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Full interactive version with multimedia resources available 
in complete edition.

Start your premium learning journey today! 🚀
"""