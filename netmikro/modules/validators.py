from re import match


def validate_ip(ip):
    """
    Validate if ip is valid

    :param ip: Ip to be validated
    :return: True if ip is valid, False otherwise
    """
    return match(r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$', ip)
