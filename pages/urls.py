from django.urls import path

from .views import HomePageView, AboutPageView, PubProviderList, PubProductList, PubProductDetailView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("pub-products/", PubProductList.as_view(), name="pub-products"),
    path("pub-providers/", PubProviderList.as_view(), name="pub-providers"),
    path("pub-product/<int:pk>/", PubProductDetailView.as_view(), name="pub-product-detail"),
]
