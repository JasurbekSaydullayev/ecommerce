from django.urls import path

from .views import AccountDetailView, AccountListView

urlpatterns = [
    path('users-list/', AccountListView.as_view(), name='user-list'),
    path('user-detail/', AccountDetailView.as_view(), name='user-detail-api'),
]
