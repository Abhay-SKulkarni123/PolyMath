from django.contrib import admin
from .models import VendorProfile

# Register your models here.
@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'store_name', 'is_approved', 'created_at']
    list_filter = ['is_approved']
    search_fields = ['use__email', 'store_name']