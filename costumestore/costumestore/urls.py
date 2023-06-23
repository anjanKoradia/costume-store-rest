from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/", include("products.urls")),
    path("api/cart/", include("cart.urls")),
    path("api/accounts/", include("accounts.urls")),
    path("api/auth/", include("authentication.urls")),
    path("admin/", admin.site.urls),
]
