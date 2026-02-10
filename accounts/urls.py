from django.urls import path
from .views import (
    register_view,
    login_view,
    logout_view,
    verify_email_view,
    verification_pending_view,
)

app_name = "accounts"

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("verify-email/<str:token>/", verify_email_view, name="verify_email"),
    path("verification-pending/<str:username>/", verification_pending_view, name="verification_pending"),
]