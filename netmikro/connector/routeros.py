from time import sleep
from datetime import date, time
from typing import Dict, List, Optional, Union

from netmiko.mikrotik.mikrotik_ssh import MikrotikRouterOsSSH

from netmikro.modules import validate_ip

from .._utils import convert


# noinspection PyUnresolvedReferences
class RouterOS:
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
        self.identity = self._get('/system/identity/get name')
        self.note = self._get('/system/note/get note')
        self.model = self._get('/system/routerboard/get model')

    def __str__(self):
        return self.identity

    def _get(self, command: str) -> Optional[str]:
        output = self.cmd(f'return [{command}]')
        if output == '':
            return None
        return output

    def disconnect(self):
        """
        Disconnects the router's connection.

        Examples:
            >>> router.disconnect()
        """
        return self._connection.disconnect()

    def cmd(self, command: str) -> str:
        """
        Runs a command in the router's terminal.

        Parameters:
            command: Command to be executed

        Returns:
            Output of the command

        Examples:
            >>> router.cmd('/system identity print')
            'name: Netmikro'
        """
        return self._connection.send_command(command)

    def cmd_multiline(self, commands: List[str]):
        """
        Runs multiple commands in the router's terminal.

        Parameters
            commands: List of commands to be executed

        Returns:
            Output of the commands

        Examples:
            >>> router.cmd_multiline([
            ...     '/system identity print',
            ...     '/system note print'
            ... ])
            ['name: Netmikro', 'note: Test']
        """
        return self._connection.send_multiline(commands)

    def clock_time_get(self) -> time:
        """
        Returns the router's system time.

        Returns:
            Time with time zone, an instance of the `time` class.

        Examples:
            >>> router.clock_time_get()
            datetime.time(5, 41, 24)
            >>> router.clock_time_get().isoformat()
            '15:30:00'
        """
        clock_time = self._get('/system clock get time').split(':')
        return time(*[int(i) for i in clock_time])

    def clock_date_get(self) -> date:
        """
        Returns the router's system date.

        Returns:
            An instance of the `date` class.

        Examples:
            >>> router.clock_date_get()
            datetime.date(2020, 12, 31)
            >>> router.clock_date_get().isoformat()
            '2020-12-31'
        """
        clock_date = self._get('/system clock get date').split('-')
        return date(*[int(i) for i in clock_date])

    def clock_time_zone_get(self) -> str:
        """
        Returns the router's time zone.

        Returns:
            Time zone in the format Continent/City

        Examples:
            >>> router.clock_time_zone_get()
            'America/Cuiaba'
        """
        return self._get('/system clock get time-zone-name')

    def clock_gmt_offset_get(self) -> str:
        """
        Returns the router's GMT offset.

        Returns:
            GMT offset in the format +/-HH:MM

        Examples:
            >>> router.clock_gmt_offset_get()
            '-04:00'
        """
        return self._get('/system/clock/get gmt-offset as-string')

    def clock_dst_active_get(self) -> Optional[bool]:
        """
        Returns True if DST is enabled, if not enabled, returns False.

        Returns:
            True if DST is enabled, if not enabled, returns False.
        """
        return convert(self._get('/system clock get dst-active'))

    def clock_time_zone_autodetect_get(self) -> Optional[bool]:
        """
        Returns True if time-zone-autodetect is enabled,
        if not enabled, it returns False.

        Returns:
            True if time-zone-autodetect is enabled,
            if not enabled, returns False.
        """
        return convert(self._get('/system clock get time-zone-autodetect'))

    def health_voltage(self) -> float:
        """
        Returns the current voltage at the router

        Returns:
            Voltage in Volts

        Examples:
            >>> router.health_voltage()
            24.0
        """
        output = self._get('/system/health/get number=0 value')
        return float(output)

    def health_temperature(self) -> float:
        """
        Returns the current temperature at the router

        Returns:
            Temperature in Celsius

        Examples:
            >>> router.health_temperature()
            40.0
        """
        output = self._get('/system/health/get number=1 value')
        return float(output)

    def history_system_get(self) -> str:
        """
        Returns the history of changes made to the router's
        system settings during the time it has been running uninterrupted.

        Returns:
            History of changes made to the router's system settings

        Examples:
            >>> router.history_system_get()
            Flags: U - UNDOABLE
            Columns: ACTION, BY, POLICY
              ACTION                        BY    POLICY
            U ntp settings changed          hick  write
            U changed system note settings  hick  write
            U changed system note settings  hick  write
            U ip service changed            hick  write
        """
        output = self.cmd('/system history print')
        return output

    def identity_set(self, new_identity: str):
        """
        Sets the router's identity.

        Parameters:
            new_identity: New identity to be set

        Examples:
            >>> router.identity_set('new_identity')
        """
        new_identity.strip()
        self.cmd(f'/system identity set name={new_identity}')
        sleep(2)
        self.identity = new_identity
        return self.identity

    def note_set(self, note: str, show_at_login: bool = False):
        """
        Sets the router's note.

        Parameters:
            note: New note to be set
            show_at_login: Specifies whether a new note should be
                displayed every time a user logs into the router.

        Examples:
            >>> router.note_set('new_note', True)
        """
        show_at_login = 'yes' if show_at_login else 'no'
        self.cmd(
            f'/system note set note="{note}" show-at-login={show_at_login}'
        )

    def ntp_client_get(self) -> Dict[str, Union[bool, str, int, List[str]]]:
        """
        Returns the NTP client configuration.

        Returns:
            Dictionary with the NTP client configuration

        Examples:
            >>> router.ntp_client_get()
            {
                'enabled': True,
                 'freq-diff': '3.082 PPM',
                 'mode': 'unicast',
                 'servers': ['200.160.7.186', '201.49.148.135'],
                 'status': 'synchronized',
                 'synced-server': '200.160.7.186',
                 'synced-stratum': 1,
                 'system-offset': -0.915,
                 'vrf': 'main'
            }
        """

        ntp_command = '/system ntp client get'
        servers = self._get(f'{ntp_command} servers').split(';')

        return {
            'enabled': convert(self._get(f'{ntp_command} enabled')),
            'mode': self._get(f'{ntp_command} mode'),
            'servers': servers,
            'vrf': self._get(f'{ntp_command} vrf'),
            'freq-dift': self._get(f'{ntp_command} freq-drift as-string'),
            'status': self._get(f'{ntp_command} status'),
            'synced-server': self._get(f'{ntp_command} synced-server'),
            'synced-stratum': int(self._get(f'{ntp_command} synced-stratum')),
            'system-offset': self._get(f'{ntp_command} system-offset as-string')
        }

    def ntp_client_set(
        self,
        servers: List[str],
        enabled: bool = True,
        mode: str = 'unicast',
        vrf: str = 'main',
    ):
        """
        Sets the NTP client configuration.

        Parameters:
            servers: Comma separated list of NTP servers
            enabled: Specifies whether the NTP client should be enabled
            mode: Specifies the NTP client mode
            vrf: Specifies the VRF to be used by the NTP client

        Examples:
            >>> router.ntp_client_set(
                '200.160.7.186, 201.49.148.135',
                True,
                'unicast',
                'main'
            )
        """

        for ip_server in servers:
            if not validate_ip(ip_server):
                raise ValueError(f'Invalid IP: {ip_server}')
        servers = ','.join(servers)

        enabled = 'yes' if enabled else 'no'
        mode = mode.lower().strip()
        if mode not in ['unicast', 'broadcast', 'multicast', 'manycast']:
            raise ValueError(f'Invalid mode: {mode}')
        vrf = vrf.lower().strip()

        self.cmd(
            f'/system ntp client set '
            f'enabled={enabled} mode={mode} servers={servers} vrf={vrf}'
        )

        return None

    def ntp_server_get(self) -> dict[str, Union[bool, str, None]]:
        """
        Returns the NTP server configuration.

        Returns:
            Dictionary with the NTP server configuration

        Examples:
            >>> router.ntp_server_get()
            {
                'broadcast': False,
                'broadcast-address': None,
                'enabled': False,
                'manycast': False,
                'multicast': False,
                'vrf': 'main'
            }
        """
        ntp_command = '/system ntp server get'
        return {
            'enabled': convert(self._get(f'{ntp_command} enabled')),
            'broadcast': convert(self._get(f'{ntp_command} broadcast')),
            'multicast': convert(self._get(f'{ntp_command} multicast')),
            'manycast': convert(self._get(f'{ntp_command} manycast')),
            'broadcast-address': self._get(f'{ntp_command} broadcast-address'),
            'vrf': self._get(f'{ntp_command} vrf'),
        }
