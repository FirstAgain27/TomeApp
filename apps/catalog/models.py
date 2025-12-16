from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify


class Book(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название книги'
    )

    author = models.ForeignKey(
        'Author',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books',
        verbose_name='Автор'
    )

    isbn = models.CharField(
        max_length=13,  # ISBN-13
        unique=True,
        verbose_name='ISBN',
        help_text='13 символов'
    )
    
    # Описание
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    
    # Категории
    categories = models.ManyToManyField(
        'Category',
        related_name='books',
        verbose_name='Категории'
    )
    
    # Цена и наличие
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена',
        validators=[MinValueValidator(0)]
    )
    
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена со скидкой',
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    
    stock_quantity = models.PositiveIntegerField(
        verbose_name='Количество на складе',
        default=0
    )
    
    # Издательство
    publisher = models.CharField(
        max_length=100,
        verbose_name='Издательство',
        blank=True
    )
    
    publication_date = models.DateField(
        verbose_name='Дата публикации',
        null=True,
        blank=True
    )
    
    # Технические детали
    pages = models.PositiveIntegerField(
        verbose_name='Количество страниц',
        null=True,
        blank=True
    )
    
    language = models.CharField(
        max_length=50,
        verbose_name='Язык',
        default='Русский'
    )
    
    cover_type = models.CharField(
        max_length=20,
        verbose_name='Тип обложки',
        choices=[
            ('hard', 'Твёрдая'),
            ('soft', 'Мягкая'),
            ('electronic', 'Электронная'),
        ],
        default='soft'
    )
    
    # Изображения
    cover_image = models.ImageField(
        upload_to='books/covers/',
        verbose_name='Обложка',
        blank=True
    )
    
    # Рейтинг и популярность
    average_rating = models.FloatField(
        verbose_name='Средний рейтинг',
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    
    rating_count = models.PositiveIntegerField(
        verbose_name='Количество оценок',
        default=0
    )
    
    # Для SEO и URL
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True
    )
    
    # Метаданные
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.title}-{self.isbn}')
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.author} - {self.title}'
    
    @property
    def in_stock(self):
        return self.stock_quantity > 0
    
    @property
    def current_price(self):
        return self.discount_price or self.price
    
    @property
    def pages_count(self):
        return f'Количество страниц: {self.pages}'
    
    @property
    def has_discount(self):
        return self.discount_price is not None
    
    @property
    def discount_percentage(self):
        if self.has_discount and self.price > 0:
            return int((1 - self.discount_price / self.price) * 100)
        return 0
    
    # Meta класс
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['isbn']),
            models.Index(fields=['average_rating']),
            models.Index(fields=['price']),
        ]
    

class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    second_name = models.CharField(max_length=100, verbose_name='Фамилия')
    bio = models.TextField(verbose_name='Биография', blank=True)
    photo = models.ImageField(upload_to='authors/', blank=True)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.second_name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.first_name} {self.second_name}")
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.full_name
    
    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['second_name', 'first_name']

    
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey( # позволяет организовать категории в дерево с родителями и детьми
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    


