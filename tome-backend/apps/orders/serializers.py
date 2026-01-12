from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import Order

class OrderListSerializer(serializers.ModelSerializer):
    """Список заказов"""
    items_count = serializers.SerializerMethodField()
    formatted_date = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'order_number',
            'items_count',
            'status',
            'formatted_date',
            'total_price'
        ]

    def get_items_count(self, obj):
        """Количество товаров в заказе"""
        return obj.items.count()
    
    def get_formatted_date(self, obj):
        """Дата в красивом формате"""
        months = ['янв', 'фев', 'мар', 'апр', 'май', 'июн', 
                  'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
        return f"{obj.created_at.day} {months[obj.created_at.month-1]} {obj.created_at.year}"


class OrderCreateSerializer(serializers.ModelSerializer):
    """Создание заказа"""
    shipping_address = serializers.CharField(required=True, min_length=10, max_length=500)
    phone_number = serializers.CharField(
        required=True, 
        validators=[RegexValidator(r'^\+?7?\d{10}$')] # Валидация формата номера телефона
        )
    class Meta:
        model = Order
        fields = [
            'shipping_address',
            'phone_number',
            'payment_method'
        ]
        # Только те данные, которые необходимы для создания заказа


class OrderAdminUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для редактирования заказа (Только для админа)"""
    class Meta:
        model = Order
        fields = ['status'] # поменять можно только статус заказа


class OrderCancelSerializer(serializers.Serializer):
    reason = serializers.CharField(required=True, max_length=500)  # Причина отмены
    
    def validate(self, attrs):
        order = self.context.get('order')
        if not order:
            raise serializers.ValidationError("Заказ не найден")
        
        if order.status not in ['PENDING', 'PAID']:
            raise serializers.ValidationError('Нельзя отменить доставленный заказ')
        return attrs 
    
"""TODO: OrderItemSerializer, OrderDetailSerializer"""