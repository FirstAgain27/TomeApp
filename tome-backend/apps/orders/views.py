from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Order, OrderItem
from apps.cart.models import CartItem
from rest_framework.response import Response
from .serializers import (OrderCreateSerializer,
                          OrderListSerializer,
                          OrderDetailSerializer,
                          OrderAdminUpdateSerializer,
                          OrderCancelSerializer,
                          OrderNoteAddSerializer
                          )


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с Order"""

    def get_permissions(self):
        """Разные права для разных действий"""
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """Получаем queryset в зависимости от прав"""
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """Отдельный сериализатор на каждое действие"""
        if self.action == 'list':
            return OrderListSerializer
        elif self.action == 'retrieve':
            return OrderDetailSerializer
        elif self.action == 'create':
            return OrderCreateSerializer
        elif self.action in ['update', 'partial_update']:
            if self.request.user.is_staff:
                return OrderAdminUpdateSerializer
            
        return OrderDetailSerializer
    
    def create(self, request, *args, **kwargs):
        """Метод создания заказа"""
        serializer = OrderCreateSerializer(
            data=request.data, 
            context = {'request' : request}
            )
        
        serializer.is_valid(raise_exception=True)
        
        cart_items = CartItem.objects.filter(cart=request.user.cart)

        if not cart_items.exists():
            return Response({
                'error' : 'Корзина пуста. Для оформления заказа добавьте товары в корзину',
            }, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(
            item.book.price * item.quantity 
            for item in cart_items
        )

        order = Order.objects.create(
            user = request.user, 
            shipping_address = serializer.validated_data['shipping_address'],
            phone_number = serializer.validated_data['phone_number'],
            payment_method = serializer.validated_data['payment_method'], 
            total_price = total_price,
            # status='PENDING', payment_status='PENDING' установятся по default
            # order_number сгенерируется в save() методе модели
        )

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,                    # ссылка на созданный Order
                book=cart_item.book,            # книга из корзины
                quantity=cart_item.quantity,    # количество из корзины
                price=cart_item.book.price,     # текущая цена книги 
                # Сохраняем исторические данные если есть поля в модели:
                # title=cart_item.book.title,
                # author_name=cart_item.book.author_name
            )
     
        cart_items.delete()

        return Response(OrderDetailSerializer(order).data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None, *args, **kwargs):
        """Метод отмены заказа"""
        order = self.get_object()
        serializer = OrderCancelSerializer(data=request.data, context = {'request' : request})
        
        serializer.is_valid(raise_exception=True)
        
        """ Можно отменить заказ только если он в обработке или оплачен, 
        для остальных статусов - возвращаем error"""
        if order.status not in ['PAID', 'PENDING']: 
            return Response({
                'error' : f'Нельзя отменить заказ со статусом {order.status}'},
                status=status.HTTP_400_BAD_REQUEST
                )
        
        order.status = 'CANCELED'
        order.cancellation_reason = serializer.validated_data['reason']

        order.save()

        return Response({
            'message': 'Заказ успешно отменен',
            'order_id': order.id,
            'order_number': order.order_number,
            'new_status': order.status
        })
    
    @action(detail=True, methods=['post'])
    def add_note(self, request, pk=None, *args, **kwargs):
        """Метод для добавления заметки к заказу"""
        order = self.get_object()
        serializer = OrderNoteAddSerializer(
            data=request.data, 
            context = {'request' : request,
                       'order' : order})

        serializer.is_valid(raise_exception=True)

        order.note = serializer.validated_data['note']
        order.save()

        return Response({'note' : order.note}, status=status.HTTP_200_OK)

 