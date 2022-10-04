from rest_framework import mixins, viewsets

from products.models import Provider, WhLocation
from .serializers import ProviderSerializer, WhLocationSerializer

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

# product_list_view = ProductGenericViewSet.as_view({'get': 'list'})
# product_detail_view = ProductGenericViewSet.as_view({'get': 'retrieve'})