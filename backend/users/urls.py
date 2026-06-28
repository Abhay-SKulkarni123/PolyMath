from django.urls import path
from .views import (
    RegisterView, 
    LoginView, 
    MeView,
    PasswordChangeView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    EmailVerificationView,
    HealthCheckView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', MeView.as_view(), name='me'),
    path('password/change/', PasswordChangeView.as_view(), name='password-change'),
    path('password/reset/request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('email/verify/', EmailVerificationView.as_view(), name='email-verify'),
    path('health/', HealthCheckView.as_view(), name='health-check'),
]
