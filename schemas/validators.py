import phonenumbers


#* Validators  
def validate_phone(value):
    try:
        parsed_number = phonenumbers.parse(value, None)
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValueError("Invalid phone number")
    except phonenumbers.NumberParseException:
        raise ValueError("Invalid phone number format")
    return value