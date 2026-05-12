from django.db import models

# Create your models here.
class VendorProfile(models.Model):
    user = models.OneToOneField(
        'users.User',          # which model does this point to?
        on_delete=models.CASCADE,   # what happens when user is deleted?
        related_name='vendor_profile'      # how do we access this from user?
    )
    store_name = models.CharField(max_length=255)
    store_description = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} - Vendor Profile'  # what makes sense to return here?