def convert(string: str) -> bool or None or str:
    string = string.strip()
    if string == 'true':
        return True
    elif string == 'false':
        return False
    elif string == '':
        return None
    return string
