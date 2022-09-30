from django.urls import path

from . import views
# from .views import api_home


# /api/
urlpatterns = [
    path('', views.api_home), # localhost:8000/api/
    # path('products/', include('products.urls'))
]
