from rest_framework.routers import DefaultRouter


from apiproducts.viewsets import WhLocationGenericViewSet, ProviderViewSet

router = DefaultRouter()
router.register('whlocations', WhLocationGenericViewSet, basename='apiproducts')
router.register('providers', ProviderViewSet, basename='apiproducts')
urlpatterns = router.urls