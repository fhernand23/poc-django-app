from email.policy import default
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime  # for checking renewal date range.

from django import forms


class AddProductUnitForm(forms.Form):
    move_date = forms.DateField()
    quantity = forms.IntegerField(min_value=0)
    add_qr = forms.BooleanField(required=False)
    lot = forms.CharField(max_length=120, required=False)
    description = forms.CharField(max_length=240, required=False)
