from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Category, Author, Book
from .serializers import (
    CategoryListSerializer,
    CategoryMenuSeriilizer
)

class CategoryMenuView(generics.ListAPIView):
    serializer_class = CategoryMenuSeriilizer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Category.objects.order_by('name')[:5]
        
    

