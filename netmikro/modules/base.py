from typing import Optional

from netmiko.mikrotik.mikrotik_ssh import MikrotikRouterOsSSH

from ..utils.common import IpAddress


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
        self.host = IpAddress(host)
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

    def _get(self, command: str) -> Optional[str]:
        output = self._connection.send_command(
            command_string=f'return [{command}]'
        )
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

        # The `expect_string` parameter is a regex (format: [admin@mikrotik])
        # necessary in case the router's identity is changed,
        # there is no ReadTimeout error due to the output format changing,
        # as it includes the router's identity
        return self._connection.send_command(
            command_string=command,
            expect_string=rf'\[{self.username}@[^]]+\]',
        )
