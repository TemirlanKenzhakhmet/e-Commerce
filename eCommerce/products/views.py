import random
from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from item.models import Item
from .serializers import UserSerializer, ProductSerializer
from .producer import publish

class ProductViewset(viewsets.ViewSet):
    def list(self, request):
        products = Item.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_created', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        product = Item.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        product = Item.objects.get(pk=pk)
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_updated', serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk=None):
        product = Item.objects.get(pk=pk)
        product.delete()
        publish('product_deleted', pk)
        return Response('Item deleted')


class UserAPIView(APIView):
    def get(self, _):
        users = User.objects.all()
        return Response(UserSerializer(users, many=True).data)
    

class UserDetailAPIView(APIView):
    def get_user(self, pk):
        try:
            User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        user = self.get_user(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
