from django.contrib import admin

from .models import VendorProfile


# Register your models here.
@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "company_name", "is_verified", "rating", "total_sales", "created_at"]
    list_filter = ["is_verified", "created_at"]
    search_fields = ["user__email", "company_name"]
