def validate_port(port: int):
    """
    Validate if port is valid

    :param port: Port to be validated
    :return: True if port is valid, False otherwise
    """
    if port < 1 or port > 65535:
        raise ValueError(f'Invalid port: {port}')
    return
