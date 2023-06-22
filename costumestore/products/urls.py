from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

vendor_product_router = DefaultRouter()
vendor_product_router.register(
    "products", views.VendorProduct, basename="vendor_product"
)

product_router = DefaultRouter()
product_router.register("", views.ProductView)

urlpatterns = [
    path("vendor/", include(vendor_product_router.urls)),
    path("products/", include(product_router.urls)),
]
