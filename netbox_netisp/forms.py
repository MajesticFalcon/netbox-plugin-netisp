from django import forms
from utilities.forms import BootstrapMixin

from .models import Customer

class CustomerForm(BootstrapMixin, forms.ModelForm):

    class Meta:
        model = Customer
        fields = (
            'first_name',
            'middle_name',
            'last_name',
            'slug',
        )

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

    slug = forms.SlugField(
        required=True,
        label="Slug",
    )

    class Meta:
        model = Customer
        fields = []