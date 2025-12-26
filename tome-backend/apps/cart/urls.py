from rest_framework.routers import DefaultRouter
from .views import CartViewSet, CartItemViewSet

router = DefaultRouter()
router.register(r'', CartViewSet, basename='cart')  # /api/v1/cart/
router.register(r'items', CartItemViewSet, basename='cart-item')  # /api/v1/cart/items/

urlpatterns = router.urls