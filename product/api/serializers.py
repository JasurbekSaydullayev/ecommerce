from rest_framework import serializers

from category.api.serializers import CategorySerializer
from product.models import Product, Size, Color


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('id', 'name')


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ('id', 'name')


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    color = ColorSerializer()
    size = SizeSerializer()

    class Meta:
        model = Product
        fields = '__all__'


class ProductSerializerForOrder(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'quantity', 'seller', 'size', 'color')
