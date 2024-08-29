from typing import Union

from netmikro.exceptions import UndefinedBooleanValue


def boolean(string: str) -> Union[bool, None, str]:
    """Convert a string to a boolean value.

    Args:
        string (str): String to be converted.

    Returns:
        Union[bool, None]: Boolean value of the string or None if the string is empty.
    """
    string = string.strip()
    if string == 'true':
        return True
    elif string == 'false':
        return False
    elif not string:
        return None
    else:
        raise UndefinedBooleanValue(f'Undefined boolean value: {string}')
