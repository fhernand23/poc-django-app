from rest_framework import serializers

from products.models import Product, Provider, WhLocation, ProductPackaging, Client


class ProductSerializer(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = [
            'pk',
            'name',
            'short_description',
            'price',
            'sale_price',
            'my_discount',
        ]
    
    def get_my_discount(self, obj):
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, Product):
            return None
        return obj.get_discount()


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = [
            'pk',
            'cuit',
            'name',
            'contact',
        ]


class WhLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhLocation
        fields = [
            'pk',
            'name',
            'description',
        ]


class ProductPackagingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPackaging
        fields = [
            'pk',
            'name',
            'description',
        ]


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'pk',
            'name',
            'cuit',
            'contact',
        ]
