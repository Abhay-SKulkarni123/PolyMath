from django.db import models
from users.models import User


class VendorProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='vendor_profile'
    )
    company_name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    tax_id = models.CharField(max_length=50, blank=True)
    is_verified = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_sales = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.email} - {self.company_name or "Vendor"}'

    class Meta:
        db_table = 'vendor_profiles'
        verbose_name = 'Vendor Profile'
        verbose_name_plural = 'Vendor Profiles'