from django.contrib import admin
from .models import Product, ProductUnit, Provider


admin.site.register(Product)
admin.site.register(ProductUnit)
admin.site.register(Provider)
