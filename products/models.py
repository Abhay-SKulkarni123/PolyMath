from django.db import models
from django.utils.text import slugify

# Create your models here.
class KnowledgeField(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.CharField(blank=True)
    icon = models.CharField(max_length=10, blank=True)
    color = models.CharField(max_length=7, default='#000000')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'knowledge_fields'
        verbose_name = 'Knowledge Fields' 
        verbose_name_plural = 'Knowledge Fields'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.icon} {self.name}'
    
class Product(models.Model):

    TYPE_CHOICES = [
        ('physical', 'Physical'),
        ('digital', 'Digital'),
        ('experience', 'Experience'),
    ]

    vendor = models.ForeignKey(
        'vendors.VendorProfile',
        on_delete=models.CASCADE,
        related_name='products'
    )
    knowledge_fields = models.ManyToManyField(
        KnowledgeField,
        related_name = 'products',
        blank=True
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='physical'
    )
    file = models.FileField(
        upload_to='digital_products/',
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'products'
        verbose_name = 'Products'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name
        
    @property
    def is_digital(self):
        return self.type in ['digital', 'experience']