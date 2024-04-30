from netmikro.modules.base import Base

from ..utils import boolean


class Ip(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_port = self._get('/ip service get api port')
        self.api_ssl_port = self._get('/ip service get api-ssl port')
        self.ftp_port = self._get('/ip service get ftp port')
        self.ssh_port = self._get('/ip service get ssh port')
        self.telnet_port = self._get('/ip service get telnet port')
        self.winbox_port = self._get('/ip service get winbox port')
        self.http_port = self._get('/ip service get www port')
        self.https_port = self._get('/ip service get www-ssl port')

        self.api_port_disabled = boolean(
            self._get('/ip service get api disabled')
        )
        self.api_ssl_port_disabled = boolean(
            self._get('/ip service get api-ssl disabled')
        )
        self.ftp_port_disabled = boolean(
            self._get('/ip service get ftp disabled')
        )
        self.ssh_port_disabled = boolean(
            self._get('/ip service get ssh disabled')
        )
        self.telnet_port_disabled = boolean(
            self._get('/ip service get telnet disabled')
        )
        self.winbox_port_disabled = boolean(
            self._get('/ip service get winbox disabled')
        )
        self.http_port_disabled = boolean(
            self._get('/ip service get www disabled')
        )
        self.https_port_disabled = boolean(
            self._get('/ip service get www-ssl disabled')
        )
