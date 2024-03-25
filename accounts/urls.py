from django.urls import path

from .views import SignUpView, CreateVendorView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("vendor/", CreateVendorView.as_view(), name="create-vendor"),
]
