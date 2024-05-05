from dataclasses import dataclass

from netmikro.modules.base import Base

from ..utils import validate_port


@dataclass
class IpService:
    """Class for representing ip service on a MikroTik router.

    Attributes:
        port (int): Port number of the service.
        disabled (bool): Whether the service is disabled or not.
        available_from (str): IP address from which the service is available.

    Examples:
        >>> service = IpService(8728, False, '192.168.88.1')
    """

    port: int
    disabled: bool
    available_from: str


# noinspection PyUnresolvedReferences
class Ip(Base):
    """Class that generates the connection with a MikroTik router.

    Attributes:
        service (dict): Dictionary with the services available on the router.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        _service_names = [
            'api',
            'api-ssl',
            'ftp',
            'ssh',
            'telnet',
            'winbox',
            'www',
            'www-ssl',
        ]

        self.service = {
            service: IpService(
                port=int(self._get(f'/ip service get {service} port')),
                disabled=self._get_bool(f'/ip service get {service} disabled'),
                available_from=self._get(f'/ip service get {service} address'),
            )
            for service in _service_names
        }

    def ip_port_set(self, service_name: str, port: int) -> None:
        """Set the API port number.

        Args:
            service_name: The service to be changed.
            port: The new port number.

        Examples:
            >>> router.ip_port_set('www', 8080)
        """
        validate_port(port)
        self.cmd(f'/ip service set {service_name} port={port}')
        self.service[service_name].port = port
