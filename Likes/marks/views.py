import requests
from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework import mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .models import Product, Owner
from .serializers import ProductSerializer, ProductOwnerSerializer
from .producer import publish

class ProductViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class ProductOwnerViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = ProductOwnerSerializer
    queryset = Owner.objects.all()

@api_view(['GET'])
def like(request, pk, format=None):

    query = {'username': 'GayLord'}
    req = requests.get('http://127.0.0.1:8000/api/users/', params=query)
    data = req.json()
    print(data)


    try:
        for s in range(len(data)):
            if data[s]['id']:
                owner = Owner.objects.create(owner_id=data[s]['id'], product_id=pk)
                owner.save()
                publish('product_liked', pk)
                print('Owner created')
                return Response('Product liked...', status=status.HTTP_201_CREATED)
    except:
        return Response("Product already liked...", status=status.HTTP_400_BAD_REQUEST)