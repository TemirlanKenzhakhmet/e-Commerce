from rest_framework import serializers

from .models import Product, Owner

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
class ProductOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'