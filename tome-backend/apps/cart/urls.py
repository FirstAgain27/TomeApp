from rest_framework.routers import DefaultRouter
from .views import CartViewSet, CartItemViewSet
from django.urls import path, include

# Router для Cart
cart_router = DefaultRouter()
cart_router.register(r'', CartViewSet, basename='cart')

# Router для CartItem  
cart_item_router = DefaultRouter()
cart_item_router.register(r'', CartItemViewSet, basename='cart-item')

urlpatterns = [
    path('', include(cart_router.urls)),  # /api/v1/cart/
    path('items/', include(cart_item_router.urls)),  # /api/v1/cart/items/
]