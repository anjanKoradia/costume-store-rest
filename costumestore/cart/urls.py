from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()
routers.register("", views.CartView, basename="cart")

urlpatterns = [
    path("", include(routers.urls)),
    path("<str:operation>/", include(routers.urls))
]
