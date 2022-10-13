from email.policy import default
from django.core.exceptions import ValidationError
from .models import WhLocation, Provider, Client, ProductPackaging

from django import forms


locations_set = WhLocation.objects.all()
providers_set = Provider.objects.all()
clients_set = Client.objects.all()
packaging_set = ProductPackaging.objects.all()

class AddProductUnitForm(forms.Form):
    move_date = forms.DateField()
    quantity = forms.IntegerField(min_value=0)
    packaging = forms.ModelChoiceField(queryset=packaging_set)
    provider = forms.ModelChoiceField(queryset=providers_set, required=False)
    lot = forms.CharField(max_length=120, required=False)
    add_qr = forms.BooleanField(required=False)
    description = forms.CharField(max_length=240, required=False)
    wh_location = forms.ModelChoiceField(queryset=locations_set, required=False)
