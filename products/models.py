from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.TextField(max_length=255, unique=True)
    description = models.CharField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category' 
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
class Product(models.Model):
    vendor = models.ForeignKey(
        'vendors.VendorProfile',
        on_delete=models.CASCADE,
        related_name='products'
    )
    categories = models.ManyToManyField(
        Category,
        related_name = 'products',
        blank=True
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'products'
        verbose_name = 'Products'
        verbose_name_plural = 'Products'

        def __str__(self):
            return self.name
