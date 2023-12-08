from crispy_forms.helper import FormHelper
from django import forms
from .models import Address

class ShippingForm(forms.ModelForm):

    helper = FormHelper()

    class Meta:
        model = Address
        exclude = ["user"]