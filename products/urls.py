from django.urls import path
from .views import (ProviderListView, ProviderDetailView, ProductListView, ProductDetailView, 
                    ProductCreate, ProductDelete, ProductUpdate,
                    ProviderCreate, ProviderDelete, ProviderUpdate)

urlpatterns = [
    path("products/", ProductListView.as_view(), name="products"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("providers/", ProviderListView.as_view(), name="providers"),
    path("providers/<int:pk>/", ProviderDetailView.as_view(), name="provider-detail"),
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
