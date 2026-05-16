from django.db import models

# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carts'

    def __str__(self):
        return f'{self.user.email} - Cart'
    
    @property
    def total_price(self):
        return sum(
            item.product.price * item.quantity
            for item in self.items.all()
        )
    
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'cart_items'
        unique_together = ['cart', 'product']

    def __str__(self):
        return f'{self.cart.user.email} - {self.product.sum} x{self.quantity}'
    
    @property
    def item_total(self):
        return self.product.price * self.quantity