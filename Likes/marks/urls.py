from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProductOwnerViewSet, ProductViewSet, like

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('owners', ProductOwnerViewSet, basename='owners')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/like/', like, name='like')
]