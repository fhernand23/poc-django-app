from django.contrib import admin
from .models import (Product, ProductUnit, Provider, WhLocation, ProductMove, ProductMoveType, ProductPackaging,
                     Client, LogisticUnitCode)


admin.site.register(WhLocation)
admin.site.register(ProductPackaging)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Administration object for Author models.
    Defines:
     - fields to be displayed in list view (list_display)
     - orders fields in detail view (fields),
       grouping the date fields horizontally
     - adds inline addition of books in author view (inlines)
    """
    list_display = ('name', 'cuit', 'contact', 'date_created')
    fields = ['name', 'cuit', 'contact', 'documentation', 'archived']


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'cuit', 'contact', 'date_created')
    fields = ['name', 'cuit', 'contact', ('documentation', 'avatar'), 'archived']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'code', 'date_created', 'date_updated')
    fields = ['name', 'price', 'short_description', 'description', ('code', 'image'), 'archived']


@admin.register(ProductUnit)
class ProductUnitAdmin(admin.ModelAdmin):
    list_display = ('product', 'provider', 'quantity', 'wh_location', 'date_created', 'date_updated')
    fields = [('product', 'provider'), ('quantity', 'unit_valuation'), 
              ('code', 'uid'),
              ('wh_location', 'product_packaging'), ('user', 'lot'),
              ('expiration_date', 'related_moves')]


@admin.register(ProductMove)
class ProductMoveAdmin(admin.ModelAdmin):
    list_display = ('product', 'move_type', 'provider', 'client', 'quantity', 'wh_location_to', 'date_created', 'date_updated')
    fields = [('product', 'move_type'), ('provider', 'client'), 
              ('wh_location_to', 'product_packaging'), 
              ('move_date', 'lot'), 
              ('quantity'), 
              ('unit_price', 'unit_taxes', 'total_price'), 
              ('new_unit_price', 'new_unit_taxes', 'new_total_price'), 
              ('user', 'uid'), ('expiration_date', 'related_units')]


@admin.register(LogisticUnitCode)
class LogisticUnitCodeAdmin(admin.ModelAdmin):
    list_display = ('entity', 'entity_id', 'description', 'entity_url', 'entity_api_url', 'date_created')
    fields = [('entity', 'entity_id'), 'description', 
              ('rfid_code', 'qr_code'),
              'entity_url', 'entity_api_url']


@admin.register(ProductMoveType)
class ProductMoveTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    fields = ['name', 'description']
