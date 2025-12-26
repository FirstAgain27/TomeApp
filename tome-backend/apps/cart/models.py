from django.db import models
from django.db.models import Sum, F

from apps.accounts.models import User
from apps.catalog.models import Book

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_items(self):
        result = self.items.aggregate(total=models.Sum('quantity'))
        return result['total'] or 0
    
    
    def total_price(self):
        """Общая стоимость всей корзины"""
        result = self.items.aggregate(
            total=Sum(F('quantity') * F('book__price'))
        )
        return result['total'] or 0

    def __str__(self):
        return f"Корзина {self.user.email} ({self.total_items()} товаров)"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ['cart', 'book']

    def get_own_price(self):
        return self.quantity * self.book.price
    
    def __str__(self) -> str:
        return f"{self.quantity} * {self.book.title}"
    



    
    
    

    



