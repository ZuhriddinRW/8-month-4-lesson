from django.urls import path
from .views import SignUpView, VerifyCode, ResendCodeView, ChangeUserInfo

urlpatterns = [
    path ( 'signup/', SignUpView.as_view () ),
    path ( 'verify_code/', VerifyCode.as_view () ),
    path ( 'resend_code/', ResendCodeView.as_view () ),
    path ( 'change_user_info/', ChangeUserInfo.as_view() )
]