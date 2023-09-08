from netmiko import ConnectHandler

from netmikro.modules import validate_ip


class RouterOS:
    """
    Class that generates the connection with a MikroTik router.

    Attributes:
        host (str): IP address of the router you want to connect to.
        username (str): Username to be used in the connection.
        password (str): Password to be used in the connection.
        ssh_port (int): Router's SSH port.

    Examples:
        >>> from netmikro import RouterOS # doctest: +SKIP
        >>> router = RouterOS( # doctest: +SKIP
        ...     '192.168.3.3',
        ...     'test',
        ...     'test',
        ...     22,
        ...     1
        ... )
        >>> router.cmd('/system identity print') # doctest: +SKIP
        'name: test'

    Todo:
        # To implement:

        ## System
        * backup
        * console
        * default-configuration
        * device-mode
        * leds
        * license
        * logging
        * package
        ...
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
        self.auth = {
            'device_type': 'mikrotik_routeros',
            'host': host,
            'username': username,
            'password': password,
            'port': ssh_port,
            'global_delay_factor': delay,
        }
        self.connection = ConnectHandler(**self.auth)
        self.identity = self.connection.send_command(
            '/system identity print'
        ).split(': ')[1]
        self.note = self.cmd('/system note print').split(': ')[2]
        self.model = self.cmd('return [/system/routerboard/get model]')

    def cmd(self, command: str) -> str:
        """
        Runs a command in the router's terminal.

        Parameters:
            command: Command to be executed

        Returns:
            Output of the command

        Examples:
            >>> from netmikro import RouterOS # doctest: +SKIP
            >>> router = RouterOS( # doctest: +SKIP
            ...     '192.168.3.3',
            ...     'test',
            ...     'test',
            ...     22,
            ...     1
            ... )
            >>> router.cmd('/system identity print') # doctest: +SKIP
            'name: test'
        """
        return self.connection.send_command(command, delay_factor=self.delay)

    def clock_time_get(self) -> str:
        """
        Returns the router's system time.

        Returns:
            Time in the format HH:MM:SS

        Examples:
            >>> from netmikro import RouterOS # doctest: +SKIP
            >>> router = RouterOS( # doctest: +SKIP
            ...     '192.168.3.3',
            ...     'test',
            ...     'test',
            ...     22,
            ...     1
            ... )
            >>> router.clock_time_get() # doctest: +SKIP
            '15:30:00' # doctest: +SKIP
        """
        return self.cmd('return [/system clock get time]')

    def clock_date_get(self) -> str:
        """
        Returns the router's system date.

        Returns:
            Date in the format YYYY-MM-DD

        Examples:
            >>> from netmikro import RouterOS # doctest: +SKIP
            >>> router = RouterOS( # doctest: +SKIP
            ...     '192.168.3.3',
            ...     'test',
            ...     'test',
            ...     22,
            ...     1
            ... )
            >>> router.clock_date_get() # doctest: +SKIP
            '2020-12-31'
        """
        return self.cmd('return [/system clock get date]')

    def clock_time_zone_get(self) -> str:
        """
        Returns the router's time zone.

        Returns:
            Time zone in the format Continent/City

        Examples:
            >>> from netmikro import RouterOS # doctest: +SKIP
            >>> router = RouterOS( # doctest: +SKIP
            ...     '192.168.3.3',
            ...     'test',
            ...     'test',
            ...     22,
            ...     1
            ... )
            >>> router.clock_time_zone_get() # doctest: +SKIP
            'America/Cuiaba'
        """
        return self.cmd('return [/system clock get time-zone-name]')

    def clock_gmt_offset_get(self) -> str:
        """
        Returns the router's GMT offset.

        Returns:
            GMT offset in the format +/-HH:MM

        Examples:
            >>> from netmikro import RouterOS # doctest: +SKIP
            >>> router = RouterOS( # doctest: +SKIP
            ...     '192.168.3.3',
            ...     'test',
            ...     'test',
            ...     22,
            ...     1
            ... )
            >>> router.clock_gmt_offset_get() # doctest: +SKIP
            '-04:00'
        """
        output = self.connection.send_command('/system clock print')
        output = output.split(': ')[5]
        return output.split('\n')[0]

    def clock_dst_active_get(self) -> bool:
        """
        Returns True if DST is enabled, if not enabled, returns False.

        Returns:
            True if DST is enabled, if not enabled, returns False.
        """
        if self.cmd('return [/system clock get dst-active]') == 'false':
            return False
        else:
            return True

    def clock_time_zone_autodetect_get(self) -> bool:
        """
        Returns True if time-zone-autodetect is enabled,
        if not enabled, it returns False.

        Returns:
            True if time-zone-autodetect is enabled,
            if not enabled, returns False.
        """
        if (
            self.cmd('return [/system clock get time-zone-autodetect]')
            == 'false'
        ):
            return False
        else:
            return True

    def health_voltage(self) -> float:
        """
        Returns the current voltage at the router

        Returns:
            Voltage in Volts

        Examples:
            >>> from netmikro import RouterOS # doctest: +SKIP
            >>> router = RouterOS( # doctest: +SKIP
            ...     '192.168.3.3',
            ...     'test',
            ...     'test',
            ...     22,
            ...     1
            ... )
            >>> router.health_voltage() # doctest: +SKIP
            24.0
        """
        output = self.connection.send_command('/system health print')
        output = output.split(' ')
        output = [i for i in output if i != '']
        return float(output[8])

    def health_temperature(self) -> float:
        """
        Returns the current temperature at the router

        Returns:
            Temperature in Celsius

        Examples:
            >>> from netmikro import RouterOS # doctest: +SKIP
            >>> router = RouterOS( # doctest: +SKIP
            ...     '192.168.3.3',
            ...     'test',
            ...     'test',
            ...     22,
            ...     1
            ... )
            >>> router.health_temperature() # doctest: +SKIP
            40.0
        """
        output = self.connection.send_command('/system health print')
        output = output.split(' ')
        output = [i for i in output if i != '']
        return float(output[12])

    def history_system_get(self) -> str:
        """
        Returns the history of changes made to the router's
        system settings during the time it has been running uninterrupted.

        Returns:
            History of changes made to the router's system settings

        Examples:
            >>> from netmikro import RouterOS # doctest: +SKIP
            >>> router = RouterOS( # doctest: +SKIP
            ...     '192.168.3.3',
            ...     'test',
            ...     'test',
            ...     22,
            ...     1
            ... )
            >>> router.history_system_get() # doctest: +SKIP
            Flags: U - UNDOABLE
            Columns: ACTION, BY, POLICY
              ACTION                        BY    POLICY
            U ntp settings changed          hick  write
            U changed system note settings  hick  write
            U changed system note settings  hick  write
            U ip service changed            hick  write

        Todo:
            * Improve the way this information is returned to the user.
        """
        output = self.connection.send_command('/system history print')
        return output

    def identity_set(self, new_identity: str):
        """
        Sets the router's identity.

        Parameters:
            new_identity: New identity to be set

        Examples:
            >>> from netmikro import RouterOS # doctest: +SKIP
            >>> router = RouterOS( # doctest: +SKIP
            ...     '192.168.3.3',
            ...     'test',
            ...     'test',
            ...     22,
            ...     1
            ... )
            >>> router.identity_set('new_identity') # doctest: +SKIP
        """
        new_identity.strip()
        self.connection.send_command(
            f'/system identity set name={new_identity}'
        )

    def note_set(self, note: str, show_at_login: bool = False):
        """
        Sets the router's note.

        Parameters:
            note: New note to be set
            show_at_login: Specifies whether a new note should be
                displayed every time a user logs into the router.

        Examples:
            >>> from netmikro import RouterOS # doctest: +SKIP
            >>> router = RouterOS( # doctest: +SKIP
            ...     '192.168.3.3',
            ...     'test',
            ...     'test',
            ...     22,
            ...     1
            ... )
            >>> router.note_set('new_note', True) # doctest: +SKIP
        """
        show_at_login = 'yes' if show_at_login else 'no'
        self.connection.send_command(
            f'/system note set note="{note}" show-at-login={show_at_login}'
        )

    def ntp_client_get(self) -> dict:
        """
        Returns the NTP client configuration.

        Returns:
            Dictionary with the NTP client configuration

        Examples:
            >>> from netmikro import RouterOS # doctest: +SKIP
            >>> router = RouterOS( # doctest: +SKIP
            ...     '192.168.3.3',
            ...     'test',
            ...     'test',
            ...     22,
            ...     1
            ... )
            >>> router.ntp_client_get() # doctest: +SKIP
            {
                'enabled': True,
                 'freq-diff': 3.082,
                 'mode': 'unicast',
                 'servers': ['200.160.7.186', '201.49.148.135'],
                 'status': 'synchronized',
                 'synced-server': '200.160.7.186',
                 'synced-stratum': 1,
                 'system-offset': -0.915,
                 'vrf': 'main'
            }
        """
        ntp_client = self.connection.send_command(
            '/system ntp client print'
        ).split(': ')
        enabled = ntp_client[1].split('\n')[0]

        if enabled == 'yes':
            enabled = True
        else:
            enabled = False

        mode = ntp_client[2].split('\n')[0]
        servers = ntp_client[3].split('\n')[0].split(',')
        vrf = ntp_client[4].split('\n')[0]
        freq_diff = float(ntp_client[5].split('\n')[0].split(' ')[0])
        status = ntp_client[6].split('\n')[0]
        synced_server = ntp_client[7].split('\n')[0]
        synced_stratum = int(ntp_client[8].split('\n')[0][0])
        system_offset = float(ntp_client[9].split('\n')[0].split(' ')[0])
        return {
            'enabled': enabled,
            'mode': mode,
            'servers': servers,
            'vrf': vrf,
            'freq-diff': freq_diff,
            'status': status,
            'synced-server': synced_server,
            'synced-stratum': synced_stratum,
            'system-offset': system_offset,
        }

    def ntp_client_set(
        self,
        servers: str,
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
            >>> from netmikro import RouterOS # doctest: +SKIP
            >>> router = RouterOS( # doctest: +SKIP
            ...     '192.168.3.3',
            ...     'test',
            ...     'test',
            ...     22,
            ...     1
            ... )
            >>> router.ntp_client_set( # doctest: +SKIP
                '200.160.7.186, 201.49.148.135',
                True,
                'unicast',
                'main'
            )
        """
        servers = servers.replace(' ', '')
        servers_validate = servers.split(',')
        for ip_server in servers_validate:
            if not validate_ip(ip_server):
                raise ValueError(f'Invalid IP: {ip_server}')
        enabled = 'yes' if enabled else 'no'
        mode = mode.lower().strip()
        if mode not in ['unicast', 'broadcast', 'multicast', 'manycast']:
            raise ValueError(f'Invalid mode: {mode}')
        vrf = vrf.lower().strip()

        self.connection.send_command(
            f'/system ntp client set '
            f'enabled={enabled} mode={mode} servers={servers} vrf={vrf}'
        )

        return None

    def ntp_server_get(self) -> dict:
        """
        Returns the NTP server configuration.

        Returns:
            Dictionary with the NTP server configuration

        Examples:
            >>> from netmikro import RouterOS # doctest: +SKIP
            >>> router = RouterOS( # doctest: +SKIP
            ...     '192.168.3.3',
            ...     'test',
            ...     'test',
            ...     22,
            ...     1
            ... )
            >>> router.ntp_server_get() # doctest: +SKIP
            {
                'broadcast': False,
                'broadcast-address': None,
                'enabled': False,
                'manycast': False,
                'multicast': False,
                'vrf': 'main'
            }

        Todo:
            * Provide an example of a real case with a configured NTP server.
        """
        ntp_server = self.connection.send_command(
            '/system ntp server print'
        ).split(': ')
        enabled = ntp_server[1].split('\n')[0]

        if enabled == 'yes':
            enabled = True
        else:
            enabled = False

        broadcast = ntp_server[2].split('\n')[0]

        if broadcast == 'yes':
            broadcast = True
        else:
            broadcast = False

        multicast = ntp_server[3].split('\n')[0]

        if multicast == 'yes':
            multicast = True
        else:
            multicast = False

        manycast = ntp_server[4].split('\n')[0]

        if manycast == 'yes':
            manycast = True
        else:
            manycast = False

        broadcast_address = ntp_server[5].split('\n')[0]

        if broadcast_address == '':
            broadcast_address = None

        vrf = ntp_server[6].split('\n')[0]

        return {
            'enabled': enabled,
            'broadcast': broadcast,
            'multicast': multicast,
            'manycast': manycast,
            'broadcast-address': broadcast_address,
            'vrf': vrf,
        }
