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
    
    def get_categories_info(self, obj):
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
        
        
class AuthorCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления и редактирования авторов"""
    class Meta:
        model = Author
        fields = [
            'first_name', 'second_name', 'bio', 
            'photo', 'birth_date', 'death_date'
        ]

    def validate(self, data):
        birth_date = data.get('birth_date')
        death_date = data.get('death_date')
        if birth_date and death_date and birth_date > death_date:
            raise serializers.ValidationError({
                "death_date" : 'Дата смерти не может быть раньше даты рождения',
            })
        return data 
        
        
class AuthorListSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения авторов"""
    books_count = serializers.IntegerField(source='books.count', read_only=True)
    
    class Meta:
        model = Author
        fields = [
            'id', 'first_name', 'second_name', 'bio', 
            'photo', 'birth_date', 'death_date', 'slug'
        ]
        read_only_fields = fields

    

class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления категории"""
    parent = serializers.SlugRelatedField( # определяет как будет искаться поле в запросе пользователя
        queryset=Category.objects.all(),
        slug_field='slug',  # ← Используем slug вместо ID
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Category
        fields = ['name', 'parent', 'description']
    
    def validate(self, data):
        parent = data.get('parent')
        name = data.get('name')
        instance = self.instance
        
        # Проверка на цикличность
        if instance and parent and parent.id == instance.id:
            raise serializers.ValidationError({
                'parent': 'Категория не может быть своим собственным родителем'
            })
        
        # Проверка уникальности имени (с учётом того, что slug будет сгенерирован из имени)
        if name:
            # Преобразуем имя в slug для проверки
            potential_slug = slugify(name)
            
            # Ищем существующие категории с таким slug
            existing = Category.objects.filter(slug=potential_slug)
            if instance:  # При обновлении исключаем текущую категорию
                existing = existing.exclude(id=instance.id)
            
            if existing.exists():
                raise serializers.ValidationError({
                    'name': f'Категория с похожим названием уже существует (будет создан slug "{potential_slug}")'
                })
        
        return data
    
    def create(self, validated_data):
        # Автоматически генерируем slug из имени
        name = validated_data.get('name')
        if name:
            validated_data['slug'] = slugify(name)
            # Проверяем уникальность slug и добавляем суффикс если нужно
            base_slug = validated_data['slug']
            counter = 1
            while Category.objects.filter(slug=validated_data['slug']).exists():
                validated_data['slug'] = f"{base_slug}-{counter}"
                counter += 1
        
        return super().create(validated_data)
    
class CategoryShortSerializer(serializers.ModelSerializer):
    """Упрощенный сериализатор для вложенных категорий (без детей)"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']
        read_only_fields = fields
    
class CategoryListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка категорий (меню)"""
    children = serializers.SerializerMethodField(read_only=True)
    books_count = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 
                 'parent', 'children', 'books_count']
        read_only_fields = fields
    
    def get_children(self, obj):
        children = obj.children.all()
        if children:
            return CategoryShortSerializer(children, many=True).data
    
    def get_books_count(self, obj):
        """Количество книг в этой категории"""
        return obj.books.count()  # Используем related_name='books' из модели Book
    
    
    

