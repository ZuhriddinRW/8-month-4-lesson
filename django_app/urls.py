from django.urls import path
from .views import SignUpView, VerifyCode, ResendCodeView

urlpatterns = [
    path ( 'signup/', SignUpView.as_view () ),
    path ( 'verify_code/', VerifyCode.as_view () ),
    path ( 'resend_code/', ResendCodeView.as_view () )
]