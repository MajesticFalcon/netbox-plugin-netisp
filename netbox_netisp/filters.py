import django_filters
from django.db.models import Q

from .models import Customer, Address


class CustomerFilterSet(django_filters.FilterSet):

    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )

    first_name = django_filters.CharFilter(
        lookup_expr="icontains",
    )

    last_name = django_filters.CharFilter(
        lookup_expr="icontains",
    )

    class Meta:
        model = Customer

        fields = [
            "first_name",
            "last_name",
        ]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = Q(first_name__icontains=value) | Q(last_name__icontains=value)
        return queryset.filter(qs_filter)

class AddressFilterSet(django_filters.FilterSet):
    q = django_filters.CharFilter(
        method="search",
        label="Search",
    )
    
    class Meta:
        model = Address

        fields = [
            "street_number",
            "street_name",
           
        ]

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip(): 
            return queryset
        qs_filter = Q(street_name__icontains=value) | Q(street_number__icontains=value)
        return queryset.filter(qs_filter)