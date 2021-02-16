"""Unit tests for netbox-netisp ."""


from django.test import TestCase
from netbox_netisp.models import Customer, Address
from datetime import datetime

class CustomerTestCase(TestCase):
    """Test the Customer"""
    def setUp(self):
        """Create a customer object with sample data"""
        Customer.objects.create(
            first_name="Schylar",
            middle_name="S",
            last_name="Utley",
            birthdate=datetime(1997,2,10,16,13,49,71549)
        )

    def test_customer_name(self):
        """Verify that the name is being joined correctly"""
        sutley = Customer.objects.get(first_name="Schylar")
        self.assertEqual(sutley.name(), 'Schylar S Utley')

    def test_customer_age(self):
        """Verify that the customer has a valid age"""
        sutley = Customer.objects.get(first_name="Schylar")
        self.assertGreaterEqual(sutley.age(), 1)

class AddressTestCase(TestCase):

    def setUp(self):
        addr1 = Address.objects.create(
            street_number=1502,
            street_name = "Main",
            street_suffix = "Ave",
            city = "Webb City",
            state_code = "MO",
            zip = "64870-1234",
            slug = 'f'
        )

    def test_address_name_without_ord(self):
        address = Address.objects.get(slug='f')
        self.assertEqual("1502 Main Ave, Webb City MO, 64870-1234", str(address))

    def test_address_name_with_ord(self):
        address = Address.objects.get(slug='f')
        address.street_ordinance = "S"
        self.assertEqual("1502 S. Main Ave, Webb City MO, 64870-1234", str(address))

