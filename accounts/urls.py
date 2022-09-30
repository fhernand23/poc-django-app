from rest_framework import routers
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from accounts.views import AppUserViewSet, GroupViewSet


router = routers.DefaultRouter()
router.register(r'users', AppUserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
]
