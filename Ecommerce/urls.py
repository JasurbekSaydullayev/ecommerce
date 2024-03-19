from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('category/', include('category.urls')),
    path('', include('product.urls')),
    path('order/', include('order.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
]

urlpatterns_api = [
    path('api/v1/', include('category.api.urls')),
    path('api/v1/', include('product.api.urls')),
    path('api/v1/', include('order.api.urls')),
    path('api/v1/', include('account.api.urls'))
]

urlpatterns += urlpatterns_api

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


