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
    
    




        
        
        






    


    

    



    
    