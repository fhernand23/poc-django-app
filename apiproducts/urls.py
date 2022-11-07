from rest_framework.routers import DefaultRouter
from django.urls import path, include

from . import views 
from .viewsets import WhLocationGenericViewSet, ProviderViewSet, ProductPackagingViewSet

# /api/products/
urlpatterns = [
    path('product/', views.product_list_create_view),
    path('product/<int:pk>/update/', views.product_update_view),
    path('product/<int:pk>/delete/', views.product_destroy_view),
    path('product/<int:pk>/', views.product_detail_view)
]


router = DefaultRouter()
router.register('whlocation', WhLocationGenericViewSet, basename='whlocation')
router.register('provider', ProviderViewSet, basename='provider')
router.register('packaging', ProductPackagingViewSet, basename='packaging')

urlpatterns += [
    path('', include(router.urls)),
]