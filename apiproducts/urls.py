from rest_framework.routers import DefaultRouter
from django.urls import path, include

from . import views 
from .viewsets import WhLocationGenericViewSet, ProviderViewSet, ProductPackagingViewSet, ClientViewSet

# /api/products/
urlpatterns = [
    path('product/', views.product_list_create_view),
    path('product/<int:pk>/update/', views.product_update_view),
    path('product/<int:pk>/delete/', views.product_destroy_view),
    path('product/<int:pk>/', views.product_detail_view, name="product-api-detail")
]


router = DefaultRouter()
router.register('whlocation', WhLocationGenericViewSet, basename='whlocation-api')
router.register('provider', ProviderViewSet, basename='provider-api')
router.register('packaging', ProductPackagingViewSet, basename='packaging-api')
router.register('client', ClientViewSet, basename='client-api')

urlpatterns += [
    path('', include(router.urls)),
]