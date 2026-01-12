from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Cart
from .serializers import (
    CartItemReadSerializer, 
    CartSerializer,
)


class CartViewSet(viewsets.ModelViewSet):
    """ViewSet для корзины пользователя, у одного пользователя - одна корзина"""
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    def get_object(self):
        return Cart.objects.get(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        """Перенаправляем на retrieve т.к корзина одна"""
        return self.retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """Корзина создается автоматически при регистрации, нельзя создать еще одну"""
        return Response({
            "detail" : 'Корзина создаётся автоматически при регистрации'
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def destroy(self, request, *args, **kwargs):
        """Переопределяем метод destroy, т.к корзину нельзя удалить, можно только очистить"""
        return Response({
            "detail" : "Используйте action 'clear' для очистки корзины"
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    """Кастомные action's"""
    @action(detail=False, methods=['post'])
    def clear(self, request):
        """Очистка корзины"""
        # cart = self.get_object()
        cart = Cart.objects.get(user=request.user)
        cart.items.all().delete()
        return Response({"detail" : "Корзина очищена"})
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Краткая информация о корзине(только totals)"""
        cart = self.get_object()
        return Response({
            "total_items" : cart.total_items(),
            "total_price" : cart.total_price()
        })


class CartItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Только элементы корзины текущего пользователя"""
        cart = Cart.objects.get(user=self.request.user)
        return cart 
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CartItemReadSerializer
        return CartItemReadSerializer
    
    def perform_create(self, serializer):
        # Автоматически привязываем к корзине пользователя
        cart = Cart.objects.get(user=self.request.user)
        serializer.save(cart)



