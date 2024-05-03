from typing import List

from netmikro.modules import Ip, System


# noinspection PyUnresolvedReferences
class RouterOS(Ip, System):
    """
    Class that generates the connection with a MikroTik router.

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
        super().__init__(host, username, password, ssh_port, delay)

    def cmd_multiline(self, commands: List[str]) -> str:
        """
        Runs multiple commands in the router's terminal.

        Parameters
            commands: List of commands to be executed

        Returns:
            str: Output of the commands

        Examples:
            >>> router.cmd_multiline([
            ...     '/system identity print',
            ...     '/system note print'
            ... ])
            ['name: Netmikro', 'note: Test']
        """
        return self._connection.send_multiline(commands)
