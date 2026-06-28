from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Create a default vendor account if missing, then seed books"

    def handle(self, *args, **options):
        # Try to import VendorProfile - adjust if your app structure differs
        try:
            from vendors.models import VendorProfile
        except ImportError:
            self.stdout.write(self.style.ERROR("Could not import VendorProfile from vendors.models - check your app name"))
            return

        vendor_user = User.objects.filter(email="vendor@polymath.com").first()

        if not vendor_user:
            vendor_user = User.objects.create_user(
                email="vendor@polymath.com",
                password="VendorPass123!",
                first_name="Polymath",
                last_name="Vendor",
            )
            if hasattr(vendor_user, 'role'):
                vendor_user.role = 'vendor'
                vendor_user.save()
            self.stdout.write(self.style.SUCCESS(f"Created vendor user: {vendor_user.email}"))
        else:
            self.stdout.write(f"Vendor user already exists: {vendor_user.email}")

        vendor_profile = VendorProfile.objects.filter(user=vendor_user).first()
        if not vendor_profile:
            vendor_profile = VendorProfile.objects.create(
                user=vendor_user,
                business_name="Polymath Books",
            )
            self.stdout.write(self.style.SUCCESS(f"Created VendorProfile for {vendor_user.email}"))
        else:
            self.stdout.write(f"VendorProfile already exists for {vendor_user.email}")

        self.stdout.write(self.style.SUCCESS("\nNow running seed_books...\n"))
        call_command('seed_books')