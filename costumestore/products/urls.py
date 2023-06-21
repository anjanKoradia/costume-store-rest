from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", views.VendorProduct, basename="vendor_product")

urlpatterns = [
    path("vendor/", include(router.urls)),
]
