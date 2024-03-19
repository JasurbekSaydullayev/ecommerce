from rest_framework import serializers

from order.models import Order, OrderItem
from product.api.serializers import ProductSerializer, ProductSerializerForOrder


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializerForOrder(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('product', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    orderitem = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('customer', 'total_price', 'orderitem')
