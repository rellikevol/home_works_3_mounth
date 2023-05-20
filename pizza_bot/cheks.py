

def is_number(number: str):
    if len(number) > 13 or len(number) < 11:
        return False
    for i in number:
        if not i.isdigit():
            return False
    return True