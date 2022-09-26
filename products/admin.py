from django.contrib import admin
from .models import Product, ProductUnit, Provider, WhLocation


admin.site.register(Product)
admin.site.register(ProductUnit)
admin.site.register(Provider)
admin.site.register(WhLocation)
