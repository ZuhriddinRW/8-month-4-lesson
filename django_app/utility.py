import re

from rest_framework.exceptions import ValidationError

email_regex = re.compile ( r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$' )
phone_number_regex = re.compile ( r'^\+998\s?\(?\d{2}\)?\s?\d{3}-?\d{2}-?\d{2}$' )
username_regex = re.compile ( r"^[A-Za-z][A-Za-z0-9_]{4,14}$" )


def email_or_phone(email_phone_number) :
    if re.fullmatch ( email_regex, email_phone_number ) :
        data = 'email'
    elif re.fullmatch ( phone_number_regex, email_phone_number ) :
        data = 'phone_number'
    else :
        data = {
            'success' : False,
            'message' : 'You entered wrong email or phone number'
        }

        raise ValidationError ( data )

    return data


def check_user_input_type(userinput) :
    if re.fullmatch ( email_regex, userinput ) :
        data = 'email'
    elif re.fullmatch ( phone_number_regex, userinput ) :
        data = 'phone_number'
    elif re.fullmatch ( username_regex, userinput ) :
        data = 'username'
    else :
        data = {
            'success' : False,
            'message' : 'You entered wrong email, phone number or username'
        }

        raise ValidationError ( data )

    return data