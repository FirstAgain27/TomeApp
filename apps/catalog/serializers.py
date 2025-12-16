from datetime import timezone
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Book, Category, Author
from django.utils.text import slugify

class BookCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания экземпляра Book"""
    author = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
    )
    
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True
    )

    class Meta:
        model = Book 
        fields = [
            'title', 'author', 'isbn', 'description',
            'categories', 'price', 'discount_price',
            'stock_quantity', 'publisher', 'publication_date',
            'pages', 'language', 'cover_type', 'cover_image'
            ]
        
    def create(self, data):
        """Извлекаем categories из validated_data, т.к. стандартный .create() не умеет работать с ManyToMany"""
        categories = data.pop('categories', [])
        book = super().create(data)
        book.categories.set(categories)
        return book
    
    def update(self, instance, validated_data):
        """Извлекаем categories из validated_data, т.к. стандартный .create() не умеет работать с ManyToMany"""
        categories = validated_data.pop('categories', [])
        book = super().update(instance, validated_data)

        # Обновляем связи, если переданы
        if categories is not None:
            book.categories.set(categories)
        return book

    def validate_price(self, value):
        """Проверяем ТОЛЬКО само значение цены"""
        if value < 0:
            raise serializers.ValidationError("Цена не может быть отрицательной")
        return value

    def validate_discount_price(self, value):
        """Проверяем ТОЛЬКО само значение скидочной цены"""
        if value is not None and value < 0:
            raise serializers.ValidationError("Скидочная цена не может быть отрицательной")
        return value

    def validate(self, data):
        """Сравниваем несколько полей МЕЖДУ СОБОЙ"""
        price = data.get('price')
        discount_price = data.get('discount_price')

        if price and discount_price and discount_price > price:
            raise serializers.ValidationError({
                'discount_price': 'Скидочная цена не может быть выше обычной'
            })
        
        return data


class BookListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка книг"""
    author_name = serializers.CharField(source='author.get_full_name')
    current_price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author_name', 'cover_image', 
            'current_price', 'average_rating', 'slug'
            ]
        read_only_fields = fields


class BookDetailSerializer(serializers.ModelSerializer):
    author_info = serializers.SerializerMethodField(read_only=True)
    categories_info = serializers.SerializerMethodField(read_only=True)
    current_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    in_stock = serializers.BooleanField(read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = [
            # Основная информация
            'id', 'title', 'isbn', 'description',
            
            # Связанные объекты (развернутые)
            'author_info', 'categories_info',
            
            # Цены и наличие
            'price', 'discount_price', 'current_price',
            'stock_quantity', 'in_stock', 'discount_percentage',
            
            # Детали
            'publisher', 'publication_date', 'pages',
            'language', 'cover_type',
            
            # Изображения
            'cover_image',
            
            # Рейтинг
            'average_rating', 'rating_count',
            
            # Технические поля
            'slug', 'created_at', 'updated_at'
        ]

        read_only_fields = fields

        def get_author_info(self, obj):
            if obj.author:
                return {
                    'id' : obj.author.id,
                    'full_name' : obj.author.get_full_name(),
                    'bio' : obj.author.bio,
                    'photo': obj.author.photo.url if obj.author.photo else None
                }
            return None
        
        def get_category_info(self, obj):
            """Используем генератор списков(list comprehension) для получения информации о категории"""
            return [
                {
                    'id' : category.id,
                    'name' : category.name,
                    'slug' : category.slug,
                    'description' : category.description
                }
                for category in obj.categories.all()
            ]







        
        
        






    


    

    



    
    