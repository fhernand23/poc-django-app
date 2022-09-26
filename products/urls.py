from django.urls import path
from .views import (ProviderListView, ProviderDetailView, ProviderCreate, ProviderDelete, ProviderUpdate,
                    ProductListView, ProductDetailView, ProductCreate, ProductDelete, ProductUpdate,
                    WhLocationListView, WhLocationDetailView, WhLocationCreate, WhLocationDelete, WhLocationUpdate)

urlpatterns = [
    path("products/", ProductListView.as_view(), name="products"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("providers/", ProviderListView.as_view(), name="providers"),
    path("provider/<int:pk>/", ProviderDetailView.as_view(), name="provider-detail"),
    path("whlocations/", WhLocationListView.as_view(), name="whlocations"),
    path("whlocation/<int:pk>/", WhLocationDetailView.as_view(), name="whlocation-detail"),
]

# Add URLConf to create, update, and delete products
urlpatterns += [
    path('product/create/', ProductCreate.as_view(), name='product-create'),
    path('product/<int:pk>/update/', ProductUpdate.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', ProductDelete.as_view(), name='product-delete'),
]

# Add URLConf to create, update, and delete provider
urlpatterns += [
    path('provider/create/', ProviderCreate.as_view(), name='provider-create'),
    path('provider/<int:pk>/update/', ProviderUpdate.as_view(), name='provider-update'),
    path('provider/<int:pk>/delete/', ProviderDelete.as_view(), name='provider-delete'),
]

# Add URLConf to create, update, and delete whlocation
urlpatterns += [
    path('whlocation/create/', WhLocationCreate.as_view(), name='whlocation-create'),
    path('whlocation/<int:pk>/update/', WhLocationUpdate.as_view(), name='whlocation-update'),
    path('whlocation/<int:pk>/delete/', WhLocationDelete.as_view(), name='whlocation-delete'),
]
