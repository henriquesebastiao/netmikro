from dataclasses import dataclass

from netmikro.modules.base import Base

from ..utils import validate_port


@dataclass
class IpService:
    """Class for representing ip service on a MikroTik router."""

    port: int
    disabled: bool
    available_from: str


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
        """
        validate_port(port)
        self.cmd(f'/ip service set {service_name} port={port}')
        self.service[service_name].port = port
