from django.urls import path, re_path

from .views import home, AboutPageView, homedev, devpages, NotificationsListView

urlpatterns = [
    path("", home, name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("homedev/", homedev, name='homedev'),
    path("notifications/", NotificationsListView.as_view(), name="notifications"),
    # Matches any html file starting with ui
    re_path(r'^homedev/ui*\.*', devpages, name='pages'),
]
