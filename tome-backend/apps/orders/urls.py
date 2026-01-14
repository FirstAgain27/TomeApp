from rest_framework.routers import DefaultRouter
from .views import OrderViewSet
from django.urls import path
from .views import OrderViewSet, OrderCancelView

order_router = DefaultRouter()
order_router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = order_router.urls

urlpatterns = [
    path('orders/<int:pk>/cancel/', OrderCancelView.as_view(), name='order-cancel'),
] + router.urls