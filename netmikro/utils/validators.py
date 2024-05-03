def validate_port(port: int):
    """Validate if port is valid.

    Args:
        port (int): Port to be validated.

    """
    if port < 1 or port > 65535:
        raise ValueError(f'Invalid port: {port}')
