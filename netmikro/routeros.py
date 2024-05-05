from typing import List

from netmikro.modules import Ip, System


# noinspection PyUnresolvedReferences
class RouterOS(Ip, System):
    """Class that generates the connection with a MikroTik router.

    Examples:
        >>> from netmikro import RouterOS
        >>> router = RouterOS(
        ...     '192.168.3.3',
        ...     'user',
        ...     'password',
        ...     22,
        ... )
        >>> router.cmd('/system identity print')
        'name: Netmikro'
    """

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        ssh_port: int = 22,
        delay: float = 0,
    ):
        """Class that generates the connection with a MikroTik router.

        Args:
            host (str): IP address of the router you want to connect to.
            username (str): Username to be used in the connection.
            password (str): Password to be used in the connection.
            ssh_port (int): SSH port to be used in the connection.
            delay (float): Time delay between command executions on the router.
        """
        super().__init__(host, username, password, ssh_port, delay)

    def cmd_multiline(self, commands: List[str]) -> str:
        """Runs multiple commands in the router's terminal.

        Args:
            commands (List[str]): List of commands to be executed.

        Returns:
            str: Output of the commands.

        Examples:
            >>> router.cmd_multiline([
            ...     '/system identity print',
            ...     '/system note print'
            ... ])
            ['name: Netmikro', 'note: Test']
        """
        return self._connection.send_multiline(commands)
