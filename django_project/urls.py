from rest_framework import routers
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("products/", include("products.urls")),
    path("api/", include("api.urls")),
    path("api/products/", include("apiproducts.urls")),
    path('api/v2/', include('django_project.routers')),
    path("", include("pages.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
