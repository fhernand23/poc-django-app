from rest_framework import mixins, viewsets

from products.models import Provider, WhLocation, ProductPackaging, Client
from .serializers import ProviderSerializer, WhLocationSerializer, ProductPackagingSerializer, ClientSerializer

class WhLocationGenericViewSet(viewsets.ModelViewSet):
    '''
    get -> list -> Queryset
    get -> retrieve -> Product Instance Detail View
    post -> create -> New Instance
    put -> Update
    patch -> Partial UPdate
    delete -> destroy 
    '''
    queryset = WhLocation.objects.all()
    serializer_class = WhLocationSerializer
    lookup_field = 'pk' # default


class ProviderViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    '''
    get -> list -> Queryset
    get -> retrieve -> Product Instance Detail View 
    '''
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    lookup_field = 'pk' # default


class ProductPackagingViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    get -> list -> Queryset
    get -> retrieve -> Product Instance Detail View 
    '''
    queryset = ProductPackaging.objects.all()
    serializer_class = ProductPackagingSerializer
    lookup_field = 'pk' # default


class ClientViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    '''
    get -> list -> Queryset
    get -> retrieve -> Product Instance Detail View 
    '''
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    lookup_field = 'pk' # default
