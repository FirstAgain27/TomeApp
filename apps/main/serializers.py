from datetime import timezone
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Book, Category, Author
from django.utils.text import slugify

class BookListSerializer(serializers.ModelSerializer):
    """Сериализатор вывода всех объектов класса Book(всех книг из БД)"""
    author_name = serializers.CharField(
        source='author.get_full_name',  
        read_only=True
    )
    
    current_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    
    average_rating = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Book
        fields = [
            'id', 
            'title', 
            'author_name',  
            'current_price', 
            'cover_image', 
            'average_rating'
        ]

        read_only_fields = fields


class BookCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания книги"""
    title = serializers.CharField(
        required=True, 
        max_length=200,
        help_text="Название книги"
    )
    author = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        required=True,
        help_text="ID автора"
    )  
    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all(),
        required=False,
        help_text="Список ID категорий"
    ) 
    # Явно объявляем cover_image, чтобы контролировать required
    cover_image = serializers.ImageField(
        required=False,
        help_text="Обложка книги",
        allow_null=True
    )
    
    class Meta:
        model = Book
        fields = [
            'title', 'author', 'isbn', 'description',
            'categories', 'price', 'discount_price',
            'stock_quantity', 'publisher', 'publication_date',
            'pages', 'language', 'cover_type', 'cover_image',
            'slug', 'average_rating'
        ]
        read_only_fields = [
            'slug', 'created_at', 'updated_at', 
            'rating_count', 'average_rating'
        ]

    def create(self, validated_data):
        """Метод создания экземпляра Book"""
        categories = validated_data.pop('categories', []) #create родительского класса не умеет работать с ManyToMany, поэтому извлекаем связь из validated_data.
        book = super().create(validated_data)
        book.categories.set(categories)

        return book
    
    def validate(self, data):
        """Валидация всей книги"""
        discount_price = data.get('discount_price')
        price = data.get('price')
        
        if discount_price is not None and price is not None:
            if discount_price >= price:
                raise serializers.ValidationError({
                    'discount_price': 'Цена со скидкой должна быть меньше обычной цены'
                })
        
        publication_date = data.get('publication_date')
        if publication_date and publication_date > timezone.now().date():
            raise serializers.ValidationError({
                'publication_date': 'Дата публикации не может быть в будущем'
            })
        
        stock_quantity = data.get('stock_quantity')
        if stock_quantity is not None and stock_quantity < 0:
            raise serializers.ValidationError({
                'stock_quantity': 'Количество на складе не может быть отрицательным'
            })
        
        pages = data.get('pages')
        if pages is not None and pages <= 0:
            raise serializers.ValidationError({
                'pages': 'Количество страниц должно быть положительным числом'
            })
        
        return data
    
    def validate_isbn(self, value):
        """Проверка формата ISBN"""
        clean_isbn = value.replace('-', '').replace(' ', '')
        
        if not clean_isbn.isdigit():
            raise serializers.ValidationError("ISBN должен содержать только цифры")
        
        if len(clean_isbn) not in [10, 13]:
            raise serializers.ValidationError("ISBN должен содержать 10 или 13 цифр")
        
        return value


class CategoryListSerializer(serializers.ModelSerializer):
    """Список всех категорий для отдельной страницы"""
    books_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
            'slug',
        ]
        read_only_fields = ['slug']

class CategoryMenuSeriilizer(serializers.ModelSerializer):
    """Для выпадающего меню в шапке сайта"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
        read_only_fields = ['slug']






    


    

    



    
    