"""Unit tests for netbox-netisp REST API."""


from django.test import TestCase
from models import Customer

class CustomerTestCase(TestCase):
    """Test the Customer"""
    def setUp(self):
        """Create a customer object"""
        Customer.objects.create(first_name="Schylar", middle_name="S", last_name="Utley")

    def test_customer_name(self):
        """Verify that the name is being joined correctly"""
        sutley = Customer.objects.get(first_name="Schylar")
        self.assertEqual(sutley.name(), 'Schylar S Utley')
