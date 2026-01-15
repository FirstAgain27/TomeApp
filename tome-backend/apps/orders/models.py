from django.db import models
from django.utils import timezone
from apps.accounts.models import User
from apps.catalog.models import Book

ORDER_STATUS_CHOICES = [
    ('PENDING', 'В обработке'),
    ('PAID', 'Оплачен'),
    ('SHIPPED', 'Отправлен'),
    ('DELIVERED', 'Доставлен'),
    ('CANCELLED', 'Отменен'),
]

PAYMENT_METHOD_CHOICES = [
    ('CASH', 'Наличный расчет'),
    ('CARD', 'Банковская карта'),
    ('BANK_TRANSFER', 'Банковский перевод'),
    ('SBP', 'Система быстрых платежей'),
]

PAYMENT_STATUS_CHOICES = [
    ('DONE', 'Оплата завершена'),
    ('PENDING', 'В обработке'), 
    ('ERROR', 'Ошибка оплаты'),
]

class Order(models.Model):
    """Модель для заказов"""
    order_number = models.CharField(max_length=20, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=20)
    shipping_address = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Заметка к заказу
    note = models.CharField(max_length=200, blank=True)

    # статусы
    status = models.CharField(max_length=30, choices=ORDER_STATUS_CHOICES, default='PENDING')
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=30, choices=PAYMENT_STATUS_CHOICES, default='PENDING')

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"ORD-{timezone.now().strftime('%y%m%d')}-{self.pk or 'TMP'}" # Красивые названия заказов
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    """Модель для конкретного товара в заказе"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


