from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from order.api.permissions import OrderPermission, OrderItemAuthorPermission
from order.api.serializers import OrderSerializer
from order.models import Order, OrderItem
from product.models import Product


@method_decorator(cache_page(60 * 5), name='dispatch')
class OrderList(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        orderitem = cache.get('orderitem')
        if orderitem is None:
            orderitem = Order.objects.prefetch_related('orderitem').all()
            cache.set('orderitem', orderitem)
        return orderitem


class AddOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated, OrderPermission]

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        self.check_object_permissions(self.request, product)
        order, created = Order.objects.get_or_create(customer=request.user, ordered=False)
        orderitem, item_created = OrderItem.objects.get_or_create(product=product, customer=request.user, ordered=False)
        if not item_created:
            orderitem.quantity += 1
            product.quantity -= 1
            orderitem.save()
        else:
            order.orderitem.add(orderitem)
            product.quantity -= 1
            product.save()
        return Response({"message": "Ok"}, status=status.HTTP_201_CREATED)


class RemoveOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated, OrderItemAuthorPermission]

    def post(self, request, pk):
        orderitem = get_object_or_404(OrderItem, pk=pk)
        order = Order.objects.filter(orderitem=orderitem).first()
        self.check_object_permissions(self.request, orderitem)
        orderitem.product.quantity += orderitem.quantity
        order.orderitem.remove(orderitem)
        orderitem.delete()
        return Response({"message": "Ok"}, status=status.HTTP_202_ACCEPTED)


class InkrementOrderItemView(APIView):
    permission_classes = [permissions.IsAuthenticated, OrderItemAuthorPermission]

    def post(self, request, pk):
        orderitem = get_object_or_404(OrderItem, pk=pk)
        self.check_object_permissions(self.request, orderitem)
        if not orderitem:
            return Response({"error": "OrderItem not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            orderitem.quantity += 1
            orderitem.product.quantity -= 1
            orderitem.save()
            orderitem.product.save()
        return Response({"message": "Ok"}, status=status.HTTP_200_OK)


class DekrementOrderItemView(APIView):
    permission_classes = [permissions.IsAuthenticated, OrderItemAuthorPermission]

    def post(self, request, pk):
        orderitem = get_object_or_404(OrderItem, pk=pk)
        order = Order.objects.filter(orderitem=orderitem).first()
        self.check_object_permissions(self.request, orderitem)
        if orderitem.quantity == 1:
            orderitem.product.quantity += 1
            order.orderitem.remove(orderitem)
            orderitem.delete()
        else:
            orderitem.quantity -= 1
            print(orderitem.product.quantity)
            orderitem.product.quantity += 1
            print(orderitem.product.quantity)
            orderitem.save()
        orderitem.product.save()
        return Response({"message": "Ok"}, status=status.HTTP_200_OK)
