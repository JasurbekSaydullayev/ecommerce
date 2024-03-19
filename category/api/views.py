from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import generics

from .serializers import CategorySerializer
from ..models import Category


@method_decorator(cache_page(60 * 5), name='dispatch')
class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        category = cache.get('category')
        if category is None:
            category = Category.objects.prefetch_related('products').all()
            cache.set('category', category)
        return category
