from rest_framework import routers
from .views import CustomerViewSet, AddressViewSet

router = routers.DefaultRouter()
router.register('customers', CustomerViewSet)
router.register('addresses', AddressViewSet)
urlpatterns = router.urls