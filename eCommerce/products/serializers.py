from rest_framework import serializers
from django.contrib.auth.models import User

from item.models import Item

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', )