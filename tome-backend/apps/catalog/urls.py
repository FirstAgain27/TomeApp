from django.urls import path
from . import views

app_name = 'apps.catalog'

urlpatterns = [
    # Books
    path('books/', views.BookListCreateAPIView.as_view(), name='book-list'),
    path('books/<slug:slug>/', views.BookRetrieveUpdateDestroyAPIView.as_view(), name='book-detail'),
    
    # Categories
    path('categories/', views.CategoryListCreateAPIView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', views.CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-detail'),
    
    # Authors
    path('authors/', views.AuthorListCreateAPIView.as_view(), name='author-list'),
    path('authors/<slug:slug>/', views.AuthorRetrieveUpdateDestroyAPIView.as_view(), name='author-detail'),
    
    # Special
    path('categories/<slug:slug>/books/', views.BooksByCategoryAPIView.as_view(), name='category-books'),
    path('authors/<slug:slug>/books/', views.BooksByAuthorAPIView.as_view(), name='author-books'),
    path('stats/', views.CatalogStatsAPIView.as_view(), name='catalog-stats'),
]