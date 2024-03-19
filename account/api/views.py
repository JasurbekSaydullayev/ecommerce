from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics

from .serializers import UserSerializer
from ..models import User


@method_decorator(cache_page(60 * 5), name='dispatch')
class AccountListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        user = cache.get('user')
        if user is None:
            user = User.objects.all()
            cache.set('user', user)
        return user


class AccountDetailView(APIView):
    pass
