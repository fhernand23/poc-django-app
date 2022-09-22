from django.urls import path
from .views import ProviderListView, ProviderDetailView, ProductListView, ProductDetailView

urlpatterns = [
    path("products/", ProductListView.as_view(), name="products"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("providers/", ProviderListView.as_view(), name="providers"),
    path("providers/<int:pk>/", ProviderDetailView.as_view(), name="provider-detail"),
]
