import re

from jsonschema.exceptions import ValidationError

email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
phone_number_regex = re.compile(r'^\+998\s?\(?\d{2}\)?\s?\d{3}-?\d{2}-?\d{2}$')

def email_or_phone(email_phone_number):
    if re.fullmatch(email_regex, email_phone_number):
        data = 'email'
    elif re.fullmatch(phone_number_regex, email_phone_number):
        data = 'phone_number'
    else:
        data = {
            'success': 'False',
            'message': 'You entered wrong email or phone number'
        }

        raise ValidationError(data)

    return data
















