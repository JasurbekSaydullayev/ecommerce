from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import generics
from django_filters import rest_framework as filters

from ..models import Product
from .serializers import ProductSerializer


@method_decorator(cache_page(60 * 5), name='dispatch')
class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['color', 'size']

    def get_queryset(self):
        products = cache.get('products')
        if products is None:
            products = Product.objects.select_related('category').prefetch_related('color', 'size').all()
            cache.set('products', products)
        return products


class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
