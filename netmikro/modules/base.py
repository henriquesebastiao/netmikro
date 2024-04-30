from typing import Optional

from netmiko.mikrotik.mikrotik_ssh import MikrotikRouterOsSSH


class Base:
    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        ssh_port: int = 22,
        delay: float = 0,
    ):
        """
        Class that generates the connection with a MikroTik router.

        Parameters:
            host (str): IP address of the router you want to connect to.
            username (str): Username to be used in the connection.
            password (str): Password to be used in the connection.
            ssh_port (int): SSH port to be used in the connection.
            delay (float): Time delay between command executions on the router.
        """
        self.host = host
        self.username = username
        self.password = password
        self.ssh_port = ssh_port
        self.delay = delay
        _auth = {
            'device_type': 'mikrotik_routeros',
            'host': host,
            'username': username,
            'password': password,
            'port': ssh_port,
            'global_delay_factor': delay,
        }
        self._connection = MikrotikRouterOsSSH(**_auth)
        self.api_port = self._get('/ip service get api port')
        self.api_ssl_port = self._get('/ip service get api-ssl port')
        self.ftp_port = self._get('/ip service get ftp port')
        self.ssh_port = self._get('/ip service get ssh port')
        self.identity = self._get('/system identity get name')
        self.note = self._get('/system note get note')
        self.model = self._get('/system routerboard get model')

    def __str__(self):
        return self.identity

    def _get(self, command: str) -> Optional[str]:
        output = self.cmd(f'return [{command}]')
        if output == '':
            return None
        return output

    def disconnect(self):
        return self._connection.disconnect()

    def cmd(self, command: str) -> str:
        """
        Runs a command in the router's terminal.

        Parameters:
            command: Command to be executed

        Returns:
            Output of the command
        """
        return self._connection.send_command(command)
