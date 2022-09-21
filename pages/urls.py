from django.urls import path, re_path

from .views import home, AboutPageView, PubProviderListView, PubProductListView, PubProductDetailView, homedev, devpages, NotificationsListView

urlpatterns = [
    path("", home, name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("homedev/", homedev, name='homedev'),
    path("pub-products/", PubProductListView.as_view(), name="pub-products"),
    path("pub-providers/", PubProviderListView.as_view(), name="pub-providers"),
    path("pub-product/<int:pk>/", PubProductDetailView.as_view(), name="pub-product-detail"),
    path("notifications/", NotificationsListView.as_view(), name="notifications"),
    # Matches any html file starting with ui
    re_path(r'^homedev/ui*\.*', devpages, name='pages'),
]
