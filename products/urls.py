from django.urls import path
from .views import (ProviderListView, ProviderDetailView, ProviderCreate, ProviderDelete, ProviderUpdate,
                    ClientListView, ClientDetailView, ClientCreate, ClientDelete, ClientUpdate,
                    ProductListView, ProductDetailView, ProductCreate, ProductDelete, ProductUpdate,
                    product_add_qr, product_add_stock,
                    WhLocationListView, WhLocationDetailView, WhLocationCreate, WhLocationDelete, WhLocationUpdate)

urlpatterns = [
    path("products/", ProductListView.as_view(), name="products"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("providers/", ProviderListView.as_view(), name="providers"),
    path("provider/<int:pk>/", ProviderDetailView.as_view(), name="provider-detail"),
    path("clients/", ClientListView.as_view(), name="clients"),
    path("client/<int:pk>/", ClientDetailView.as_view(), name="client-detail"),
    path("whlocations/", WhLocationListView.as_view(), name="whlocations"),
    path("whlocation/<int:pk>/", WhLocationDetailView.as_view(), name="whlocation-detail"),
]

# Add URLConf to create, update, and delete products
urlpatterns += [
    path('product/create/', ProductCreate.as_view(), name='product-create'),
    path('product/<int:pk>/update/', ProductUpdate.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', ProductDelete.as_view(), name='product-delete'),
    path('product/<int:pk>/add_qr/', product_add_qr, name='product-add-qr'),
    path('product/<int:pk>/add_stock/', product_add_stock, name='product-add-stock'),
    # path('product/<int:pk>/remove_stock/', product_remove_stock, name='product-remove-stock'),
]

# Add URLConf to create, update, and delete provider
urlpatterns += [
    path('provider/create/', ProviderCreate.as_view(), name='provider-create'),
    path('provider/<int:pk>/update/', ProviderUpdate.as_view(), name='provider-update'),
    path('provider/<int:pk>/delete/', ProviderDelete.as_view(), name='provider-delete'),
]

# Add URLConf to create, update, and delete client
urlpatterns += [
    path('client/create/', ClientCreate.as_view(), name='client-create'),
    path('client/<int:pk>/update/', ClientUpdate.as_view(), name='client-update'),
    path('client/<int:pk>/delete/', ClientDelete.as_view(), name='client-delete'),
]

# Add URLConf to create, update, and delete whlocation
urlpatterns += [
    path('whlocation/create/', WhLocationCreate.as_view(), name='whlocation-create'),
    path('whlocation/<int:pk>/update/', WhLocationUpdate.as_view(), name='whlocation-update'),
    path('whlocation/<int:pk>/delete/', WhLocationDelete.as_view(), name='whlocation-delete'),
]
