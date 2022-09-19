from django.urls import path, re_path

from .views import HomePageView, AboutPageView, PubProviderListView, PubProductListView, PubProductDetailView, homedev, devpages

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("homedev/", homedev, name='homedev'),
    # Matches any html file
    re_path(r'^.*\.*', devpages, name='pages'),
    path("pub-products/", PubProductListView.as_view(), name="pub-products"),
    path("pub-providers/", PubProviderListView.as_view(), name="pub-providers"),
    path("pub-product/<int:pk>/", PubProductDetailView.as_view(), name="pub-product-detail"),
]
