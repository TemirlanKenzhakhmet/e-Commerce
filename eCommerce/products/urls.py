from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ProductViewset,
    UserAPIView, 
    UserDetailAPIView
)

router = DefaultRouter()
router.register('products', ProductViewset, basename='products')

urlpatterns = [
    path('', include(router.urls)),
    path('users/', UserAPIView.as_view(), name='users'),
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name='user-details'),
]