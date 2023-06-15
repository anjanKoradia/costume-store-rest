from . import views
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("signup/", views.RegisterUser.as_view(), name="signup"),
    path('login/', TokenObtainPairView.as_view(), name='generate_auth_token'),
    path('refresh/token/', TokenRefreshView.as_view(), name='refresh_auth_token'),
    path("activate/<str:email_token>/", views.activate_user, name="activate_user"),
]
