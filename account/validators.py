def check_phone_number(value: str):
    if not value.startswith('+998'):
        return False
    if len(value) != 13 or not value[1:].isdigit():
        return False
    return True
