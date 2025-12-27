from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from .models import Book, Category, Author
from .serializers import (
    BookListSerializer, BookDetailSerializer, BookCreateUpdateSerializer,
    CategoryListSerializer, CategoryCreateUpdateSerializer,
    AuthorListSerializer, AuthorCreateUpdateSerializer
)


# ========== BOOK VIEWS ==========
class BookListCreateAPIView(generics.ListCreateAPIView):
    """Список книг с фильтрацией и создание новой книги"""
    queryset = Book.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categories', 'author']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at', 'title']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookListSerializer
        return BookCreateUpdateSerializer


class BookRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Детальная информация, обновление и удаление книги"""
    queryset = Book.objects.all()
    lookup_field = 'slug'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return BookCreateUpdateSerializer
        return BookDetailSerializer


# ========== CATEGORY VIEWS ==========
class CategoryListCreateAPIView(generics.ListCreateAPIView):
    """Список категорий и создание новой"""
    queryset = Category.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CategoryListSerializer
        return CategoryCreateUpdateSerializer
    
    def get_queryset(self):
        """Оптимизация запросов"""
        return Category.objects.prefetch_related('children', 'books').all()


class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Детальная информация, обновление и удаление категории"""
    queryset = Category.objects.all()
    lookup_field = 'slug'
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CategoryCreateUpdateSerializer
        return CategoryListSerializer


# ========== AUTHOR VIEWS ==========
class AuthorListCreateAPIView(generics.ListCreateAPIView):
    """Список авторов и создание нового"""
    queryset = Author.objects.all()
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AuthorListSerializer
        return AuthorCreateUpdateSerializer


class AuthorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Детальная информация, обновление и удаление автора"""
    queryset = Author.objects.all()
    lookup_field = 'slug'
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AuthorCreateUpdateSerializer
        return AuthorListSerializer


# ========== SPECIAL VIEWS ==========
class BooksByCategoryAPIView(generics.ListAPIView):
    """Список книг в определенной категории"""
    serializer_class = BookListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['price', 'created_at']
    
    def get_queryset(self):
        category_slug = self.kwargs['slug']
        return Book.objects.filter(categories__slug=category_slug)


class BooksByAuthorAPIView(generics.ListAPIView):
    """Список книг определенного автора"""
    serializer_class = BookListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['price', 'created_at']
    
    def get_queryset(self):
        author_slug = self.kwargs['slug']
        return Book.objects.filter(author__slug=author_slug)


class CatalogStatsAPIView(generics.GenericAPIView):
    """Статистика каталога"""
    permission_classes = [permissions.IsAdminUser]
    
    def get(self, request):
        stats = {
            'total_books': Book.objects.count(),
            'total_categories': Category.objects.count(),
            'total_authors': Author.objects.count(),
            'books_by_category': list(
                Category.objects.annotate(
                    book_count=Count('books')
                ).values('name', 'slug', 'book_count')
            ),
            'top_authors': list(
                Author.objects.annotate(
                    book_count=Count('books')
                ).order_by('-book_count').values('name', 'slug', 'book_count')[:10]
            ),
        }
        return Response(stats)