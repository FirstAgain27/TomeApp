from rest_framework import serializers
from .models import Cart, CartItem

from apps.catalog.serializers import BookListSerializer
from apps.catalog.models import Book


class CartItemReadSerializer(serializers.ModelSerializer):
    """Только для отображения существующих CartItem"""
    book = BookListSerializer(read_only=True)  # Вложенный объект
    item_total = serializers.DecimalField(
        source='get_own_price', 
        read_only=True,
        max_digits=10,
        decimal_places=2
    )
    
    class Meta:
        model = CartItem
        fields = ['id', 'book', 'quantity', 'item_total', 'created_at']
        read_only_fields = fields  # Всё только для чтения


class CartItemWriteSerializer(serializers.ModelSerializer):
    """Для добавления и изменения CartItem"""
    # Для создания: принимаем book_id (не book!)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        write_only=True,
        source='book'  # Маппинг на поле book модели
    )
    
    class Meta:
        model = CartItem
        fields = ['book_id', 'quantity']  # НЕТ cart!
        # id не нужен при создании
    
    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Количество не может быть меньше 1")
        if value > 99:
            raise serializers.ValidationError("Нельзя добавить более 99 штук")
        return value

    def validate(self, data):
        """Валидация на уровне всего объекта"""
        book = data.get('book')  # Теперь book уже есть в data (после source='book')
        quantity = data.get('quantity')
        
        if book and hasattr(book, 'stock_quantity') and quantity:
            if quantity > book.stock_quantity:
                raise serializers.ValidationError({
                    'quantity': f'На складе только {book.stock_quantity} шт.'
                })
        
        return data


class CartSerializer(serializers.ModelSerializer):
    """Сериализатор для объекта корзины"""
    total_items = serializers.IntegerField(source='total_items', read_only=True)
    total_price = serializers.DecimalField(
        source='total_price', 
        read_only=True,
        max_digits=10,
        decimal_places=2
        )
    """Объекты корзины (ссылаемся через сериализатор CartItem)"""
    items = CartItemReadSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id', 'user', 'items', 
            'total_items', 'total_price', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CartListSerializer(serializers.ModelSerializer):
    """Для админа: список всех корзин"""
    user_email = serializers.CharField(source='user.email')
    class Meta: 
        model = Cart
        fields = [
            'id', 'user', 'user_email', 'total_items', 'created_at'
        ]


