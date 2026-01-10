from django.urls import path
from .views import *

urlpatterns = [
    path ( 'signup/', SignUpView.as_view () ),
    path ( 'signin/', SignInView.as_view () ),
    path ( 'logout/', LogOutView.as_view () ),
    path ( 'verify_code/', VerifyCode.as_view () ),
    path ( 'resend_code/', ResendCodeView.as_view () ),
    path ( 'change_user_info/', ChangeUserInfo.as_view () ),
    path ( 'change_user_photo/', UserPhotoView.as_view () )
]