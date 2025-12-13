from django.contrib import admin
from .models import Book, Author, Category

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Что показываем в списке
    list_display = ['id', 'short_title', 'author', 'price', 'stock_display', 'created_short']
    
    # Поиск по этим полям
    search_fields = ['title', 'isbn', 'author__name']
    
    # Фильтры справа
    list_filter = ['author', 'categories', 'cover_type']
    
    # Пагинация
    list_per_page = 20
    
    # Группировка полей в форме редактирования
    fieldsets = [
        ('Основное', {
            'fields': ['title', 'author', 'isbn', 'description']
        }),
        ('Категории', {
            'fields': ['categories']
        }),
        ('Цена и наличие', {
            'fields': ['price', 'discount_price', 'stock_quantity']
        }),
        ('Детали', {
            'fields': ['publisher', 'publication_date', 'pages', 'language', 'cover_type', 'cover_image']
        }),
    ]
    
    # Удобный выбор ManyToMany
    filter_horizontal = ['categories']
    
    # Кастомные методы для отображения
    def short_title(self, obj):
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title
    short_title.short_description = 'Название'
    
    def stock_display(self, obj):
        if obj.stock_quantity == 0:
            return '❌ Нет в наличии'
        elif obj.stock_quantity < 10:
            return f'⚠️ {obj.stock_quantity} шт'
        else:
            return f'✅ {obj.stock_quantity} шт'
    stock_display.short_description = 'Наличие'
    
    def created_short(self, obj):
        return obj.created_at.strftime('%d.%m.%Y')
    created_short.short_description = 'Создана'