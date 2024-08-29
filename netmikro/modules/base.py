from ipaddress import IPv4Address

from netmiko.mikrotik.mikrotik_ssh import MikrotikRouterOsSSH

from netmikro.validators import Auth, Port


class Base:
    """Class that generates the connection with a MikroTik router.

    Args:
        host (str): IP address of the router you want to connect to.
        username (str): Username to be used in the connection.
        password (str): Password to be used in the connection.
        ssh_port (int): SSH port to be used in the connection.
        delay (float): Time delay between command executions on the router.

    Attributes:
        _auth (Auth): Credenciais necessárias para realizar conexão como roteador.
        _connection (MikrotikRouterOsSSH): Conexão com o dispositivo.
    """

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        ssh_port: int = 22,
        delay: float = 0,
    ):
        _auth = Auth(
            host=host,
            username=username,
            password=password,
            port=Port(port=ssh_port).port,
            global_delay_factor=delay,
        )

        self._connection = MikrotikRouterOsSSH(
            device_type='mikrotik_routeros',
            host=str(_auth.host),
            username=_auth.username,
            password=_auth.password,
            port=_auth.port,
            global_delay_factor=_auth.global_delay_factor,
        )

    def _cmd(self, command: str) -> str:
        """Runs a command in the router's terminal.

        Args:
            command (str): Command to be executed.

        Returns:
            str: Output of the command

        Examples:
            >>> router._cmd('/system identity print')
            'name: Netmikro'
        """
        # The `expect_string` parameter is a regex (format: [admin@mikrotik])
        # necessary in case the router's identity is changed,
        # there is no ReadTimeout error due to the output format changing,
        # as it includes the router's identity
        return self._connection.send_command(
            command_string=command,
            expect_string=rf'\[{self._username}@[^]]+\]',
        )

    def _get(self, command: str) -> str:
        """Method for returning string outputs.

        Args:
            command (str): Command to be executed.

        Returns:
            str: Output of the command.
        """
        output = self._connection.send_command(f'return [{command}]').strip()
        return output

    def _get_number(self, command: str) -> int:
        """Method for returning numeric outputs in integers.

        Args:
            command (str): Command to be executed.

        Returns:
            int: Numeric output of the command.
        """
        output = self._connection.send_command(f'return [{command}]').strip()
        if not output:
            return 0
        return int(output)

    def _get_float(self, command: str) -> float:
        """Method for returning numeric outputs in floats.

        Args:
            command (str): Command to be executed.

        Returns:
            float: Numeric output of the command.
        """
        output = self._connection.send_command(f'return [{command}]').strip()
        if not output:
            return 0.0
        return float(output)

    def _get_bool(self, command: str) -> bool:
        """Method for returning boolean outputs.

        Args:
            command (str): Command to be executed.

        Returns:
            bool: Boolean output of the command.
        """
        output = self._connection.send_command(f'return [{command}]').strip()
        if output == 'true':
            return True
        return False

    def _get_list_ips(self, command: str) -> list[IPv4Address]:
        """Method for returning lists of IP addresses.

        Args:
            command (str): Command to be executed.

        Returns:
            list[IPv4Address]: List of IP addresses.
        """
        output = (
            self._connection.send_command(f'return [{command}]')
            .strip()
            .split(';')
        )
        return [IPv4Address(ip) for ip in output]
