# backend/create_sample_books.py
import os
import django
import random
from datetime import datetime, timedelta
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.catalog.models import Book, Author, Category

# Данные для генерации с указанием авторов
BOOKS_DATA = [
    {
        "title": "Мастер и Маргарита",
        "author_first_name": "Михаил",
        "author_second_name": "Булгаков",
        "categories": ["Русская классика", "Фантастика"]
    },
    {
        "title": "Преступление и наказание",
        "author_first_name": "Фёдор",
        "author_second_name": "Достоевский",
        "categories": ["Русская классика", "Психологическая проза"]
    },
    {
        "title": "Война и мир",
        "author_first_name": "Лев",
        "author_second_name": "Толстой",
        "categories": ["Русская классика", "Исторический роман"]
    },
    {
        "title": "Анна Каренина",
        "author_first_name": "Лев",
        "author_second_name": "Толстой",
        "categories": ["Русская классика", "Роман"]
    },
    {
        "title": "1984",
        "author_first_name": "Джордж",
        "author_second_name": "Оруэлл",
        "categories": ["Антиутопия", "Зарубежная литература"]
    },
    {
        "title": "Скотный двор",
        "author_first_name": "Джордж",
        "author_second_name": "Оруэлл",
        "categories": ["Антиутопия", "Повесть"]
    },
    {
        "title": "Великий Гэтсби",
        "author_first_name": "Фрэнсис",
        "author_second_name": "Фицджеральд",
        "categories": ["Зарубежная литература", "Роман"]
    },
    {
        "title": "Над пропастью во ржи",
        "author_first_name": "Джером",
        "author_second_name": "Сэлинджер",
        "categories": ["Зарубежная литература", "Роман"]
    },
    {
        "title": "Убить пересмешника",
        "author_first_name": "Харпер",
        "author_second_name": "Ли",
        "categories": ["Зарубежная литература", "Роман"]
    },
    {
        "title": "Гордость и предубеждение",
        "author_first_name": "Джейн",
        "author_second_name": "Остин",
        "categories": ["Зарубежная литература", "Роман"]
    },
    {
        "title": "Дюна",
        "author_first_name": "Фрэнк",
        "author_second_name": "Герберт",
        "categories": ["Фантастика"]
    },
    {
        "title": "Фундамент",
        "author_first_name": "Айзек",
        "author_second_name": "Азимов",
        "categories": ["Фантастика"]
    },
    {
        "title": "О дивный новый мир",
        "author_first_name": "Олдос",
        "author_second_name": "Хаксли",
        "categories": ["Антиутопия", "Фантастика"]
    },
    {
        "title": "451 градус по Фаренгейту",
        "author_first_name": "Рэй",
        "author_second_name": "Брэдбери",
        "categories": ["Антиутопия", "Фантастика"]
    },
    {
        "title": "Братья Карамазовы",
        "author_first_name": "Фёдор",
        "author_second_name": "Достоевский",
        "categories": ["Русская классика", "Психологическая проза"]
    },
    {
        "title": "Идиот",
        "author_first_name": "Фёдор",
        "author_second_name": "Достоевский",
        "categories": ["Русская классика", "Роман"]
    },
    {
        "title": "Бесы",
        "author_first_name": "Фёдор",
        "author_second_name": "Достоевский",
        "categories": ["Русская классика", "Психологическая проза"]
    },
    {
        "title": "Мёртвые души",
        "author_first_name": "Николай",
        "author_second_name": "Гоголь",
        "categories": ["Русская классика", "Роман"]
    },
    {
        "title": "Ревизор",
        "author_first_name": "Николай",
        "author_second_name": "Гоголь",
        "categories": ["Русская классика", "Комедия", "Драма"]
    },
    {
        "title": "Евгений Онегин",
        "author_first_name": "Александр",
        "author_second_name": "Пушкин",
        "categories": ["Русская классика", "Поэзия", "Роман"]
    },
    {
        "title": "Герой нашего времени",
        "author_first_name": "Михаил",
        "author_second_name": "Лермонтов",
        "categories": ["Русская классика", "Роман"]
    },
    {
        "title": "Отцы и дети",
        "author_first_name": "Иван",
        "author_second_name": "Тургенев",
        "categories": ["Русская классика", "Роман"]
    },
    {
        "title": "Обломов",
        "author_first_name": "Иван",
        "author_second_name": "Гончаров",
        "categories": ["Русская классика", "Роман"]
    },
    {
        "title": "Собачье сердце",
        "author_first_name": "Михаил",
        "author_second_name": "Булгаков",
        "categories": ["Русская классика", "Фантастика"]
    },
    {
        "title": "Белая гвардия",
        "author_first_name": "Михаил",
        "author_second_name": "Булгаков",
        "categories": ["Русская классика", "Исторический роман"]
    },
    {
        "title": "Тихий Дон",
        "author_first_name": "Михаил",
        "author_second_name": "Шолохов",
        "categories": ["Русская классика", "Исторический роман"]
    },
]

CATEGORIES = [
    "Русская классика",
    "Зарубежная литература", 
    "Фантастика",
    "Детектив",
    "Роман",
    "Повесть",
    "Поэзия",
    "Драма",
    "Комедия",
    "Трагедия",
    "Антиутопия",
    "Биография",
    "Мемуары",
    "Исторический роман",
    "Психологическая проза"
]

def get_or_create_author(first_name, second_name):
    """Создает или получает автора, исправляя slug при необходимости"""
    # Ищем существующего автора
    author = Author.objects.filter(
        first_name=first_name,
        second_name=second_name
    ).first()
    
    if author:
        # Если у автора пустой slug, исправляем
        if not author.slug:
            base_slug = slugify(f"{first_name}-{second_name}")
            author.slug = base_slug
            # Проверяем уникальность
            counter = 1
            while Author.objects.filter(slug=author.slug).exclude(id=author.id).exists():
                author.slug = f"{base_slug}-{counter}"
                counter += 1
            author.save()
        return author
    else:
        # Создаем нового автора
        base_slug = slugify(f"{first_name}-{second_name}")
        slug = base_slug
        counter = 1
        while Author.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        author = Author.objects.create(
            first_name=first_name,
            second_name=second_name,
            bio=f'Биография {first_name} {second_name}',
            slug=slug
        )
        return author

def get_or_create_category(name):
    """Создает или получает категорию"""
    category = Category.objects.filter(name=name).first()
    
    if category:
        if not category.slug:
            category.slug = slugify(name)
            category.save()
        return category
    else:
        category = Category.objects.create(
            name=name,
            description=f'Книги в жанре {name}',
            slug=slugify(name)
        )
        return category

def create_sample_books():
    # Создаем все необходимые категории
    print("🏷️ Создаем категории...")
    for category_name in CATEGORIES:
        get_or_create_category(category_name)
    
    # Создаем книги с правильными авторами
    print("\n📚 Создаем книги...")
    books_created = 0
    
    for book_data in BOOKS_DATA:
        try:
            title = book_data["title"]
            author_first_name = book_data["author_first_name"]
            author_second_name = book_data["author_second_name"]
            category_names = book_data["categories"]
            
            # Проверяем, существует ли уже такая книга у этого автора
            existing_book = Book.objects.filter(
                title=title,
                author__first_name=author_first_name,
                author__second_name=author_second_name
            ).first()
            
            if existing_book:
                print(f"⚠️  Книга уже существует: '{title}' ({author_first_name} {author_second_name})")
                continue
            
            # Получаем или создаем автора
            author = get_or_create_author(author_first_name, author_second_name)
            
            # Создаем уникальный slug для книги
            base_slug = slugify(title)
            book_slug = base_slug
            counter = 1
            while Book.objects.filter(slug=book_slug).exists():
                book_slug = f"{base_slug}-{counter}"
                counter += 1
            
            # Создаем книгу
            book = Book.objects.create(
                title=title,
                author=author,
                isbn=f'978{random.randint(1000000000, 9999999999)}',
                description=f'Описание книги "{title}" от автора {author.full_name}.',
                price=random.randint(500, 5000),
                stock_quantity=random.randint(1, 50),
                publisher=random.choice(['АСТ', 'Эксмо', 'Азбука', 'Росмэн', 'Просвещение']),
                publication_date=datetime.now() - timedelta(days=random.randint(0, 365*5)),
                pages=random.choice([200, 300, 400, 500, 600]),
                language='Русский',
                cover_type=random.choice(['hard', 'soft']),
                average_rating=round(random.uniform(3.5, 5.0), 1),
                slug=book_slug
            )
            
            # Добавляем категории
            categories = []
            for category_name in category_names:
                category = get_or_create_category(category_name)
                categories.append(category)
            
            book.categories.set(categories)
            
            # Иногда добавляем скидку
            if random.random() > 0.7:  # 30% книг со скидкой
                book.discount_price = round(book.price * random.uniform(0.7, 0.9), 2)
                book.save()
            
            books_created += 1
            print(f"✅ Создана книга: '{title}' - {author_first_name} {author_second_name}")
            
        except Exception as e:
            print(f"❌ Ошибка создания книги '{book_data['title']}': {e}")
    
    print(f"\n🎉 Итоги:")
    print(f"📚 Создано книг: {books_created}")
    print(f"📚 Всего книг в БД: {Book.objects.count()}")
    print(f"👤 Всего авторов: {Author.objects.count()}")
    print(f"🏷️ Всего категорий: {Category.objects.count()}")

if __name__ == '__main__':
    create_sample_books()