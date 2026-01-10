from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import *
from .utility import email_or_phone, check_user_input_type
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class SignUpSerializer ( serializers.ModelSerializer ) :
    id = serializers.UUIDField ( read_only=True )
    auth_type = serializers.CharField ( read_only=True, required=False )
    auth_status = serializers.CharField ( read_only=True, required=False )
    email_phone_number = serializers.CharField ( write_only=True, required=True )

    class Meta :
        model = User
        fields = [
            'auth_type',
            'auth_status',
            'id',
            'email_phone_number'
        ]

    def create(self, validated_data) :
        validated_data.pop ( 'email_phone_number', None )

        user = super ( SignUpSerializer, self ).create ( validated_data )

        if user.auth_type == VIA_EMAIL :
            code = user.verify_code ( VIA_EMAIL )
            print ( code )
        elif user.auth_type == VIA_PHONE :
            code = user.verify_code ( VIA_PHONE )
            print ( code )
        else :
            data = {
                'success' : False,
                'message' : 'Enter phone number or email correctly'
            }
            raise ValidationError ( data )

        user.save ()
        return user

    def validate(self, data) :
        data = self.auth_validate ( data )
        return data

    @staticmethod
    def auth_validate(data) :
        user_input = str ( data.get ( 'email_phone_number' ) )
        user_input_type = email_or_phone ( user_input )

        if user_input_type == 'email' :
            data = {
                'auth_type' : VIA_EMAIL,
                'email' : user_input
            }
        elif user_input_type == 'phone_number' :
            data = {
                'auth_type' : VIA_PHONE,
                'phone_number' : user_input
            }
        else :
            data = {
                'success' : False,
                'message' : 'Enter phone number or email'
            }
            raise ValidationError ( data )

        return data

    def validate_email_phone_number(self, value) :
        value = value.lower ()
        if value and User.objects.filter ( email=value ).exists () :
            raise ValidationError ( "This email is already registered!" )
        elif value and User.objects.filter ( phone_number=value ).exists () :
            raise ValidationError ( "This phone number is already registered!" )
        return value

    def to_representation(self, instance) :
        data = super ( SignUpSerializer, self ).to_representation ( instance )
        data.update ( instance.token () )
        return data


class ResendCodeSerializer ( serializers.Serializer ) :
    email_phone_number = serializers.CharField ( write_only=True, required=True )

    def validate(self, data) :
        user_input = str ( data.get ( 'email_phone_number' ) )
        user_input_type = email_or_phone ( user_input )

        if user_input_type == 'email' :
            user = User.objects.filter ( email=user_input ).first ()
        elif user_input_type == 'phone_number' :
            user = User.objects.filter ( phone_number=user_input ).first ()
        else :
            raise ValidationError ( {
                'success' : False,
                'message' : 'Enter phone number or email correctly'
            } )

        if not user :
            raise ValidationError ( {
                'success' : False,
                'message' : 'User not found'
            } )

        data['user'] = user
        return data

    def create(self, validated_data) :
        user = validated_data.get ( 'user' )

        user.verify_codes.filter ( confirmed=False ).delete ()

        if user.auth_type == VIA_EMAIL :
            code = user.verify_code ( VIA_EMAIL )
            print ( f"New code for email: {code}" )
        elif user.auth_type == VIA_PHONE :
            code = user.verify_code ( VIA_PHONE )
            print ( f"New code for phone: {code}" )

        return user


class ChangeUserInfoSerializer ( serializers.Serializer ) :
    first_name = serializers.CharField ( required=True, write_only=True )
    last_name = serializers.CharField ( required=True, write_only=True )
    username = serializers.CharField ( required=True, write_only=True )
    password = serializers.CharField ( required=True, write_only=True )
    confirm_password = serializers.CharField ( required=True, write_only=True )

    def validate(self, data) :
        password = data.get ( 'password' )
        confirm_password = data.get ( 'confirm_password' )

        if password != confirm_password :
            raise ValidationError ( {
                'success' : False,
                'message' : "Passwords don't match"
            } )

        if password :
            validate_password ( password )

        return data

    def validate_first_name(self, value) :
        if not value.strip () :
            raise ValidationError ( "First name cannot be empty" )

        if value.isdigit () :
            raise ValidationError ( "First name should not contain only digits" )

        if len ( value ) < 2 :
            raise ValidationError ( "First name should contain at least 2 characters" )

        return value.strip ()

    def validate_last_name(self, value) :
        if not value.strip () :
            raise ValidationError ( "Last name cannot be empty" )

        if value.isdigit () :
            raise ValidationError ( "Last name should not contain only digits" )

        if len ( value ) < 2 :
            raise ValidationError ( "Last name should contain at least 2 characters" )

        return value.strip ()

    def validate_username(self, value) :
        if value.isdigit () or len ( value ) < 5 :
            raise ValidationError (
                "Username should not contain digits and should contain at least 5 characters"
            )
        return value

    def update(self, instance, validated_data) :
        validated_data.pop ( 'confirm_password', None )

        instance.username = validated_data.get ( 'username', instance.username )
        instance.first_name = validated_data.get ( 'first_name', instance.first_name )
        instance.last_name = validated_data.get ( 'last_name', instance.last_name )

        password = validated_data.get ( 'password' )
        if password :
            instance.set_password ( password )

        if instance.auth_status == CODE_VERIFIED :
            instance.auth_status = DONE

        instance.save ()
        return instance


class UserPhotoSerializer ( serializers.Serializer ) :
    photo = serializers.ImageField ()

    def update(self, instance, validated_data) :
        photo = validated_data.get ( 'photo', None )
        if photo :
            instance.photo = photo
            instance.auth_status = PHOTO_DONE

        instance.save ()
        return instance


class SignInSerializer ( TokenObtainPairSerializer ) :
    def __init__(self, instance=None, data=..., **kwargs) :
        super ( SignInSerializer, self ).__init__ ( instance, data, **kwargs )
        self.fields['user_input'] = serializers.CharField ( required=True )
        self.fields['username'] = serializers.CharField ( required=False, read_only=True )

    def auth_validate(self, data) :
        user_input = data.get ( 'user_input' )
        user_type = check_user_input_type ( user_input )
        if user_type == 'username' :
            user = User.objects.filter ( username=user_input ).first ()
            self.get_user ( user )
            username = user_input
        elif user_type == 'email' :
            user = User.objects.filter ( email__iexact=user_input ).first ()
            self.get_user ( user )
            username = user.username
        elif user_type == 'phone_number' :
            user = User.objects.filter ( phone_number=user_input ).first ()
            self.get_user ( user )
            username = user.username
        else :
            data = {
                'success' : False,
                'message' : 'Sign in failed'
            }
            raise ValidationError ( data )

        authenticated_kwargs = {
            self.username_field : username,
            'password' : data.get ( 'password' )
        }

        user = authenticate ( **authenticated_kwargs )

        if not user :
            raise ValidationError ( {
                'success' : False,
                'message' : 'Invalid credentials'
            } )

        if user.auth_status in [NEW, CODE_VERIFIED] :
            data = {
                'success' : False,
                'message' : "Not registered"
            }
            raise ValidationError ( data )

        self.user = user
        return data

    @staticmethod
    def get_user(user) :
        if not user :
            raise ValidationError ( {
                'success' : False,
                'message' : 'User not found'
            } )

    def validate(self, attrs) :
        data = self.auth_validate ( attrs )
        data = self.user.token ()
        data['auth_status'] = self.user.auth_status

        return data


class LogOutSerializer ( serializers.Serializer ) :
    refresh = serializers.CharField ( required=True )

    def validate(self, attrs) :
        self.token = attrs.get ( 'refresh' )
        return attrs

    def save(self, **kwargs) :
        try :
            token = RefreshToken ( self.token )
            token.blacklist ()
        except Exception as e :
            raise ValidationError ( {
                'success' : False,
                'message' : 'Token is invalid or expired'
            } )