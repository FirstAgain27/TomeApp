from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Book, Category, Author

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
            'pages', 'language', 'cover_type', 'cover_image'
        ]
        read_only_fields = [
            'slug', 'created_at', 'updated_at', 
            'rating_count', 'average_rating'
        ]









    
    