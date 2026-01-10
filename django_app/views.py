from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from datetime import datetime
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView


class SignUpView ( CreateAPIView ) :
    queryset = User.objects.all ()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]


class VerifyCode ( APIView ) :
    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs) :
        user = self.request.user
        code = self.request.data.get ( 'code' )

        self.check_verify_code ( user, code )
        data = {
            'success' : True,
            'auth_status' : user.auth_status,
            'access' : user.token ()['access'],
            'refresh' : user.token ()['refresh']
        }
        return Response ( data )

    @staticmethod
    def check_verify_code(user, code) :
        verify = user.verify_codes.filter (
            code=code,
            confirmed=False,
            expiration_time__gt=datetime.now ()
        )
        if not verify.exists () :
            data = {
                'success' : False,
                'message' : "Code has expired or not valid"
            }
            raise ValidationError ( data )

        verify = verify.first ()
        verify.confirmed = True
        verify.save ()

        if user.auth_status == NEW :
            user.auth_status = CODE_VERIFIED
            user.save ()

        return True


class ResendCodeView ( CreateAPIView ) :
    queryset = User.objects.all ()
    serializer_class = ResendCodeSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs) :
        serializer = self.get_serializer ( data=request.data )
        serializer.is_valid ( raise_exception=True )
        user = serializer.save ()

        data = {
            'success' : True,
            'message' : 'Verification code has been resent',
            'auth_type' : user.auth_type,
            'email' if user.auth_type == VIA_EMAIL else 'phone_number' :
                user.email if user.auth_type == VIA_EMAIL else user.phone_number
        }
        return Response ( data )


class ChangeUserInfo ( UpdateAPIView ) :
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all ()
    serializer_class = ChangeUserInfoSerializer

    def get_object(self) :
        return self.request.user

    def update(self, request, *args, **kwargs) :
        super ( ChangeUserInfo, self ).update ( request, *args, **kwargs )
        data = {
            'success' : True,
            'message' : "Updated successfully!"
        }
        return Response ( data )


class UserPhotoView ( APIView ) :
    permission_classes = [IsAuthenticated]

    def put(self, request) :
        serializer = UserPhotoSerializer ( data=request.data )
        serializer.is_valid ( raise_exception=True )
        user = self.request.user
        serializer.update ( user, validated_data=serializer.validated_data )
        data = {
            'success' : True,
            'message' : 'Your photo was changed successfully'
        }
        return Response ( data )


class SignInView ( TokenObtainPairView ) :
    serializer_class = SignInSerializer
    permission_classes = [AllowAny]


class LogOutView ( APIView ) :
    permission_classes = [IsAuthenticated]
    serializer_class = LogOutSerializer

    def post(self, request, *args, **kwargs) :
        serializer = self.serializer_class ( data=request.data )
        serializer.is_valid ( raise_exception=True )
        serializer.save ()

        data = {
            'success' : True,
            'message' : 'Successfully logged out'
        }
        return Response ( data )