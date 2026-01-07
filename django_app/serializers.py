from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import *
from .utility import email_or_phone


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