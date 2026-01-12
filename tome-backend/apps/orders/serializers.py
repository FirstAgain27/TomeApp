from rest_framework import serializers
from django.core.validators import RegexValidator
from .models import Order, OrderItem
from .models import PAYMENT_METHOD_CHOICES

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
    payment_method = serializers.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        required=True,
        error_messages={
            'required': 'Выберите способ оплаты',
            'invalid_choice': 'Неверный способ оплаты'}
        )
    
    class Meta:
        model = Order
        fields = [
            'shipping_address',
            'phone_number',
            'payment_method'
        ] # Только те данные, которые необходимы для создания заказа


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
    

class OrderItemSerializer(serializers.ModelSerializer):
    """Сериализатор для товара в заказе"""
    
    # Вычисляемые поля для удобства фронтенда
    total = serializers.SerializerMethodField()
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_author = serializers.CharField(source='book.author_name', read_only=True)
    book_cover = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = [
            'book',           # id книги (для ссылок)
            'book_title',     # "Война и мир" (для отображения)
            'book_author',    # "Лев Толстой"
            'book_cover',     # URL обложки
            'quantity',       # количество
            'price',          # цена за штуку (фиксированная!)
            'total'           # цена × количество
        ]
        read_only_fields = fields  # Все поля только для чтения!
    
    def get_total(self, obj):
        """Рассчитывает общую стоимость позиции"""
        return obj.quantity * obj.price
    
    def get_book_cover(self, obj):
        """Получает обложку книги"""
        # Проверяем, есть ли обложка у книги
        if obj.book and obj.book.cover_image:
            return obj.book.cover_image.url if hasattr(obj.book.cover_image, 'url') else obj.book.cover_image
        return None


class OrderDetailSerializer(serializers.ModelSerializer):
    """Детальная информация о заказе"""
    items = OrderItemSerializer(many=True, read_only=True)
    formatted_date = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Order
        fields = ['order_number', 'user', 'phone_number',
                  'shipping_address', 'total_price', 'status',
                  'payment_method', 'payment_status', 'updated_at', 'created_at', 'items', 'formatted_date']
        
        read_only_fields = [
        'order_number', 'user', 'total_price', 'created_at', 'updated_at',
        'items', 'payment_method', 'formatted_date']

    def get_formatted_date(self, obj):
        months = ['янв', 'фев', 'мар', 'апр', 'май', 'июн',
                  'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
        return f"{obj.created_at.day} {months[obj.created_at.month-1]} {obj.created_at.year}"

