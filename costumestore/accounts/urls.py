from . import views
from django.urls import path

urlpatterns = [
    path("vendor/profile/", views.VendorProfile.as_view(), name="vendor_profile"),
    path("address/", views.UserAddress.as_view(), name="user_address"),
]
