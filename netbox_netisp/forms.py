from django import forms
from utilities.forms import BootstrapMixin

from .models import Customer

class CustomerFilterForm(BootstrapMixin, forms.ModelForm):
    """Form for filtering BgpPeering instances."""

    q = forms.CharField(required=False, label="Search")



    first_name = forms.CharField(
        required=False,
        label="First Name",
    )

    last_name = forms.CharField(
        required=False,
        label="Last Name",
    )

    class Meta:
        model = Customer
        fields = []