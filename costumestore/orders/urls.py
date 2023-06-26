from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()
routers.register("", views.VendorOrderView, basename="vendor_order")

urlpatterns = [
    path("customer/", views.CustomerOrderView.as_view()),
    path("vendor/", include(routers.urls)),
]
