from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import *
from .utility import email_or_phone


class SignUpSerializer ( serializers.ModelSerializer ) :
    id = serializers.UUIDField ( read_only=True )
    auth_type = serializers.CharField ( read_only=True, required=False )
    auth_status = serializers.CharField ( read_only=True, required=False )

    def __init__(self, *args, **kwargs) :
        super ( SignUpSerializer, self ).__init__ ( *args, **kwargs )
        self.fields['email_phone_number'] = serializers.CharField ( read_only=True, required=False )

    class Meta :
        model = User
        fields = [
            'auth_type',
            'auth_status',
            'id'
        ]

    def create(self, validated_data) :
        user = super ( SignUpSerializer, self ).create ( validated_data )
        if user.auth_type == VIA_EMAIL :
            code = user.verify_code ( VIA_EMAIL )
        elif user.auth_type == VIA_PHONE :
            code = user.verify_code ( VIA_PHONE )
        else :
            data = {
                'success' : 'False',
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
        elif user_input == 'phone_number' :
            data = {
                'auth_type' : VIA_PHONE,
                'phone_number' : user_input
            }
        else :
            data = {
                'success' : 'False',
                'message' : 'Enter phone number or email'
            }

            raise ValidationError ( data )
        return data