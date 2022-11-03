from email.policy import default
from django.core.exceptions import ValidationError
from .models import WhLocation, Provider, Client, ProductPackaging

from django import forms


locations_set = WhLocation.objects.all()
providers_set = Provider.objects.all()
clients_set = Client.objects.all()
packaging_set = ProductPackaging.objects.all()

class InProductUnitForm(forms.Form):
    move_date = forms.DateField()
    quantity = forms.IntegerField(min_value=0)
    packaging = forms.ModelChoiceField(queryset=packaging_set)
    provider = forms.ModelChoiceField(queryset=providers_set, required=False)
    unit_price = forms.DecimalField(max_digits=8, decimal_places=2, required=False)
    unit_taxes = forms.DecimalField(max_digits=8, decimal_places=2, required=False)
    total_price = forms.DecimalField(max_digits=8, decimal_places=2, required=False)
    lot = forms.CharField(max_length=120, required=False)
    add_qr = forms.BooleanField(required=False)
    rfid_code = forms.CharField(max_length=240, required=False)
    description = forms.CharField(max_length=240, required=False)
    wh_location = forms.ModelChoiceField(queryset=locations_set, required=False)
    expiration_date = forms.DateField(required=False)


class OutProductUnitForm(forms.Form):
    move_date = forms.DateField()
    quantity = forms.IntegerField(min_value=0)
    client = forms.ModelChoiceField(queryset=clients_set, required=False)
    unit_price = forms.DecimalField(max_digits=8, decimal_places=2, required=False)
    unit_taxes = forms.DecimalField(max_digits=8, decimal_places=2, required=False)
    total_price = forms.DecimalField(max_digits=8, decimal_places=2, required=False)
    description = forms.CharField(max_length=240, required=False)
    internal_usage = forms.BooleanField(required=False)


class QualityProductUnitForm(forms.Form):
    move_date = forms.DateField()
    quantity = forms.IntegerField(min_value=0)
    description = forms.CharField(max_length=240)


class LocationProductUnitForm(forms.Form):
    move_date = forms.DateField()
    wh_location_to = forms.ModelChoiceField(queryset=locations_set, required=False)
    description = forms.CharField(max_length=240, required=False)


class GroupingProductUnitForm(forms.Form):
    move_date = forms.DateField()
    packaging_to = forms.ModelChoiceField(queryset=packaging_set)
    description = forms.CharField(max_length=240, required=False)
