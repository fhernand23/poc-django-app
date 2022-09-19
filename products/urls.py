from django.urls import path
from .views import ProviderListView, ProductListView, ProductDetailView

urlpatterns = [
    path("products/", ProductListView.as_view(), name="products"),
    path("providers/", ProviderListView.as_view(), name="providers"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
]
