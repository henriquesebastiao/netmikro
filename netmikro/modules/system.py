from datetime import date, time
from ipaddress import IPv4Address
from typing import List

from netmikro.exceptions import InvalidNtpMode
from netmikro.modules.base import Base
from netmikro.utils import boolean
from netmikro.validators import (
    IfRouterboard,
    License,
    NTPClient,
    NTPServer,
    Resources,
)


# noinspection PyUnresolvedReferences
class System(Base):
    """Gets system-related information from the router.

    Attributes:
        identity (str): Name of the router (format: 'HS-A (192.168.88.1) on RB912UAG-5HPnD (mipsbe)').
        routerboard (dict): If the router is a RouterBoard, returns a dictionary with board information.
        license (dict): A dictionary with router license information.
        note (str): Notes of about the router.
        resources (dict): A dictionary with router hardware information.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.identity: str = self._get('/system identity get name')

        if self.is_routerboard():
            # ROUTERBOARD
            prefix = '/system routerboard get'
            self.routerboard = IfRouterboard(
                model=self._get(f'{prefix} model'),
                revision=self._get(f'{prefix} revision'),
                serial_number=self._get(f'{prefix} serial-number'),
                firmware_type=self._get(f'{prefix} firmware-type'),
                factory_firmware=self._get(f'{prefix} factory-firmware'),
                current_firmware=self._get(f'{prefix} current-firmware'),
                upgrade_firmware=self._get(f'{prefix} upgrade-firmware'),
            )

            # LICENSE
            prefix = '/system license get'
            self.license = License(
                software_id=self._get(f'{prefix} software-id'),
                level=self._get_number(f'{prefix} nlevel'),
                features=self._get(f'{prefix} features'),
            )

        # NOTE
        self.note = self._get('/system note get note')

        # RESOURCES
        prefix = '/system resource get'
        self.resources = Resources(
            cpu=self._get('/system resource get cpu'),
            cpu_frequency=self._get_number(
                '/system resource get cpu-frequency'
            ),
            memory=self._get_number('/system resource get total-memory'),
            storage=self._get_number('/system resource get total-hdd-space'),
            architecture=self._get('/system resource get architecture-name'),
            board_name=self._get('/system resource get board-name'),
            version=self._get('/system resource get version'),
        )

    def __str__(self) -> str:
        return f'{self.identity} ({self._host}) on {self.resources.board_name} ({self.resources.architecture})'

    def clock_time_get(self) -> time:
        """Returns the router's system time.

        Returns:
            time: Time with time zone, an instance of the `time` class.

        Examples:
            >>> router.clock_time_get()
            datetime.time(5, 41, 24)
            >>> router.clock_time_get().isoformat()
            '15:30:00'
        """
        clock_time = self._get('/system clock get time').split(':')
        time_list = [int(i) for i in clock_time]
        return time(
            hour=time_list[0], minute=time_list[1], second=time_list[2]
        )

    def clock_date_get(self) -> date:
        """Returns the router's system date.

        Returns:
            date: An instance of the `date` class.

        Examples:
            >>> router.clock_date_get()
            datetime.date(2020, 12, 31)
            >>> router.clock_date_get().isoformat()
            '2020-12-31'
        """
        clock_date = self._get('/system clock get date').split('-')
        return date(*[int(i) for i in clock_date])

    def clock_time_zone_get(self) -> str:
        """Returns the router's time zone.

        Returns:
            str: Time zone in the format Continent/City.

        Examples:
            >>> router.clock_time_zone_get()
            'America/Cuiaba'
        """
        return self._get('/system clock get time-zone-name')

    def clock_gmt_offset_get(self) -> str:
        """Returns the router's GMT offset.

        Returns:
            str: GMT offset in the format +/-HH:MM.

        Examples:
            >>> router.clock_gmt_offset_get()
            '-04:00'
        """
        return self._get('/system clock get gmt-offset as-string')

    def clock_dst_active_get(self) -> bool:
        """Returns True if DST is enabled, if not enabled, returns False.

        Returns:
            bool: True if DST is enabled, if not enabled, returns False.

        Examples:
            >>> router.clock_dst_active_get()
            True
        """
        return self._get_bool('/system clock get dst-active')

    def clock_time_zone_autodetect_get(self) -> bool:
        """Returns True if time-zone-autodetect is enabled, if not enabled, it returns False.

        Returns:
            bool: True if time-zone-autodetect is enabled, if not enabled, returns False.

        Examples:
            >>> router.clock_time_zone_autodetect_get()
            True
        """
        return self._get_bool('/system clock get time-zone-autodetect')

    def health_voltage(self) -> float:
        """Returns the current voltage at the router.

        Returns:
            float: Voltage in Volts.

        Examples:
            >>> router.health_voltage()
            24.0
        """
        return self._get_float('/system health get number=0 value')

    def health_temperature(self) -> float:
        """Returns the current temperature at the router.

        Returns:
            float: Temperature in Celsius.

        Examples:
            >>> router.health_temperature()
            40.0
        """
        return self._get_float('/system health get number=1 value')

    def history_system_get(self) -> str:
        """Returns the history of changes made to the router's system settings.

        Returns:
            str: History of changes made to the router's system settings

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
        return self._cmd('/system history print')

    def identity_set(self, new_identity: str):
        """Sets the router's identity.

        Args:
            new_identity (str): New identity to be set.

        Examples:
            >>> router.identity_set('new_identity')
        """
        new_identity.strip()
        self._cmd(f'/system identity set name={new_identity}')
        self.identity = new_identity

    def note_set(self, note: str, show_at_login: bool = False):
        """Sets the router's note.

        Args:
            note (str): New note to be set.
            show_at_login (bool): Tells whether the user should see the note when logging in.

        Examples:
            >>> router.note_set('new_note', True)
        """
        show_at_login_command = 'yes' if show_at_login else 'no'
        self._cmd(
            f'/system note set note="{note}" show-at-login={show_at_login_command}'
        )

    def ntp_client_get(
        self,
    ) -> NTPClient:
        """Returns the NTP client configuration.

        Returns:
            dict: Dictionary with the NTP client configuration.

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
        prefix = '/system ntp client get'
        npt_client = NTPClient(
            enabled=self._get_bool(f'{prefix} enabled'),
            mode=self._get(f'{prefix} mode'),
            servers=self._get_list_ips(f'{prefix} servers'),
            vrf=self._get(f'{prefix} vrf'),
            freq_diff=self._get_number(f'{prefix} freq-drift'),
            status=self._get(f'{prefix} status'),
            synced_server=IPv4Address(self._get(f'{prefix} synced-server')),
            synced_stratum=self._get_number(f'{prefix} synced-stratum'),
            system_offset=self._get_number(f'{prefix} system-offset'),
        )

        return npt_client

    def ntp_client_set(
        self,
        servers: List[IPv4Address],
        enabled: bool = True,
        mode: str = 'unicast',
        vrf: str = 'main',
    ):
        """Sets the NTP client configuration.

        Args:
            servers (list): List of NTP servers.
            enabled (bool): Specifies whether the NTP client should be enabled.
            mode (str): Specifies the NTP client mode.
            vrf (str): Specifies the VRF to be used by the NTP client.

        Examples:
            >>> router.ntp_client_set(
                '200.160.7.186, 201.49.148.135',
                True,
                'unicast',
                'main'
            )
        """
        servers_command: str = ','.join([
            str(IPv4Address(server)) for server in servers
        ])

        enabled_command = 'yes' if enabled else 'no'
        mode = mode.lower().strip()
        if mode not in {'unicast', 'broadcast', 'multicast', 'manycast'}:
            raise InvalidNtpMode(f'Invalid mode: {mode}')
        vrf = vrf.lower().strip()

        self._cmd(
            f'/system ntp client set '
            f'enabled={enabled_command} mode={mode} servers={servers_command} vrf={vrf}'
        )

    def ntp_server_get(self) -> NTPServer:
        """Returns the NTP server configuration.

        Returns:
            dict: Dictionary with the NTP server configuration.

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
        prefix = '/system ntp server get'

        _broadcast_address = (
            IPv4Address(_broadcast_address)
            if (_broadcast_address := self._get(f'{prefix} broadcast-address'))
            else None
        )

        ntp_server = NTPServer(
            enabled=boolean(self._get(f'{prefix} enabled')),
            broadcast=boolean(self._get(f'{prefix} broadcast')),
            multicast=boolean(self._get(f'{prefix} multicast')),
            manycast=boolean(self._get(f'{prefix} manycast')),
            broadcast_address=_broadcast_address,
            vrf=self._get(f'{prefix} vrf'),
        )

        return ntp_server

    def is_routerboard(self) -> bool:
        """Returns True if the router is a RouterBoard, if not, returns False.

        Returns:
            bool: True if the router is a RouterBoard, if not, returns False.
        """
        return self._get_bool('/system routerboard get routerboard')
