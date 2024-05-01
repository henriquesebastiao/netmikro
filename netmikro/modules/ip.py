from dataclasses import dataclass

from netmikro.modules.base import Base

from ..utils import boolean, validate_port


@dataclass
class IpService:
    port: int
    disabled: bool
    available_from: None | list[str]


class Ip(Base):
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
                disabled=boolean(
                    self._get(f'/ip service get {service} disabled')
                ),
                available_from=self._get(f'/ip service get {service} address'),
            )
            for service in _service_names
        }

    def ip_port_set(self, service_name: str, port: int) -> None:
        """
        Set the API port number.

        Args:
            service_name: The service to be changed.
            port: The new port number.
        """
        validate_port(port)
        self.cmd(f'/ip service set {service_name} port={port}')
        self.service[service_name].port = port
