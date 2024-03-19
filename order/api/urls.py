from django.urls import path

from .views import OrderList, AddOrderView, RemoveOrderView, InkrementOrderItemView, DekrementOrderItemView

urlpatterns = [
    path('orders/', OrderList.as_view(), name='order_list'),
    path('orders/<int:pk>/', AddOrderView.as_view(), name='add_order'),
    path('orders/remove/<int:pk>/', RemoveOrderView.as_view(), name='remove_orderitem'),
    path('orders/inkrement/<int:pk>/', InkrementOrderItemView.as_view(), name='inkrement_orderitem'),
    path("orders/dekrement/<int:pk>/", DekrementOrderItemView.as_view(), name='dekrement_orderitem')
]
