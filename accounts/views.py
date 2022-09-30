from rest_framework import viewsets
from rest_framework import permissions
from django.contrib.auth.models import Group
from accounts.models import AppUser
from accounts.serializers import AppUserSerializer, GroupSerializer


class AppUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = AppUser.objects.all().order_by('-date_joined')
    serializer_class = AppUserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
