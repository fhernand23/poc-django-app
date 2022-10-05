from django.contrib import admin
from .models import Product, ProductUnit, Provider, WhLocation, ProductMove, ProductMoveType, ProductPackaging, Client


admin.site.register(Product)
admin.site.register(ProductUnit)
admin.site.register(Provider)
admin.site.register(WhLocation)
admin.site.register(ProductMove)
admin.site.register(ProductMoveType)
admin.site.register(ProductPackaging)
admin.site.register(Client)
