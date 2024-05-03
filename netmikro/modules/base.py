from netmiko.mikrotik.mikrotik_ssh import MikrotikRouterOsSSH

from ..utils.common import IpAddress


class Base:
    """Class that generates the connection with a MikroTik router.

    Args:
        host (str): IP address of the router you want to connect to.
        username (str): Username to be used in the connection.
        password (str): Password to be used in the connection.
        ssh_port (int): SSH port to be used in the connection.
        delay (float): Time delay between command executions on the router.

    Attributes:
        host (IpAddress): IP address of the router you want to connect to.
        username (str): Username to be used in the connection.
        password (str): Password to be used in the connection.
        ssh_port (int): SSH port to be used in the connection.
        delay (float): Time delay between command executions on the router.
    """

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        ssh_port: int = 22,
        delay: float = 0,
    ):
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

    def _get(self, command: str) -> str:
        output = self._connection.send_command(f'return [{command}]').strip()
        return output

    def _get_number(self, command: str) -> int:
        output = self._connection.send_command(f'return [{command}]').strip()
        if output == '':
            return 0
        return int(output)

    def _get_bool(self, command: str) -> bool:
        output = self._connection.send_command(f'return [{command}]').strip()
        if output == 'true':
            return True
        return False

    def _get_list_ips(self, command: str) -> list[IpAddress]:
        output = (
            self._connection.send_command(f'return [{command}]')
            .strip()
            .split(';')
        )
        return [IpAddress(ip) for ip in output]

    def disconnect(self):
        """Disconnects the connection with the router."""
        return self._connection.disconnect()

    def cmd(self, command: str) -> str:
        """Runs a command in the router's terminal.

        Args:
            command (str): Command to be executed

        Returns:
            str: Output of the command
        """
        # The `expect_string` parameter is a regex (format: [admin@mikrotik])
        # necessary in case the router's identity is changed,
        # there is no ReadTimeout error due to the output format changing,
        # as it includes the router's identity
        return self._connection.send_command(
            command_string=command,
            expect_string=rf'\[{self.username}@[^]]+\]',
        )
