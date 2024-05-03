from datetime import date, time
from typing import Dict, List, Optional, Union

from netmikro.exceptions import InvalidNtpMode
from netmikro.modules.base import Base
from netmikro.utils import IpAddress, boolean


# noinspection PyUnresolvedReferences
class System(Base):
    """Gets system-related information from the router.

    Attributes:
        identity: Name of the router (format: 'HS-A (192.168.88.1) on RB912UAG-5HPnD (mipsbe)')
        routerboard: If the router is a RouterBoard, returns a dictionary with the following keys:
            - model: RouterBoard model
            - revision: Revision version
            - serial-number: Serial number of the router
        license: A dictionary with router license information, with the following keys:
            - software-id: Software ID
            - level: License level
            - features: License features
        note: Notes of about the router
        resources: A dictionary with router hardware information, with the following keys:
            - cpu: CPU model
            - cpu-frequency: CPU frequency (MHz)
            - memory: Total RAM (Bytes)
            - storage: Total storage (Bytes)
            - architecture: Router architecture
            - board-name: Name of the board Routerboard
            - version: Router version
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.identity = self._get('/system identity get name')

        # ROUTERBOARD
        if self.is_routerboard():
            _model = self._get('/system routerboard get model')
            _revision = self._get('/system routerboard get revision')
            _serial_number = self._get('/system routerboard get serial-number')
            _firmware_type = self._get('/system routerboard get firmware-type')
            _factory_firmware = self._get(
                '/system routerboard get factory-firmware'
            )
            _current_firmware = self._get(
                '/system routerboard get current-firmware'
            )
            _upgrade_firmware = self._get(
                '/system routerboard get upgrade-firmware'
            )

            self.routerboard: dict[str, str] = {
                'model': _model,
                'revision': _revision,
                'serial-number': _serial_number,
                'firmware-type': _firmware_type,
                'factory-firmware': _factory_firmware,
                'current-firmware': _current_firmware,
                'upgrade-firmware': _upgrade_firmware,
            }

            # LICENSE
            _software_id = self._get('/system license get software-id')
            _level = self._get_number('/system license get nlevel')
            _features = self._get('/system license get features')

            self.license: dict[str, str | int] = {
                'software-id': _software_id,
                'level': _level,
                'features': _features,
            }

        # NOTE
        self.note = self._get('/system note get note')

        # RESOURCES
        _cpu = self._get('/system resources get cpu')
        _cpu_frequency = self._get_number('/system resource get cpu-frequency')
        _memory = self._get_number('/system resource get total-memory')
        _storage = self._get_number('/system resource get total-hdd-space')
        _architecture = self._get('/system resource get architecture-name')
        _board_name = self._get('/system resource get board-name')
        _version = self._get('/system resource get version')

        self.resources: dict[str, str | int] = {
            'cpu': _cpu,
            'cpu-frequency': _cpu_frequency,
            'memory': _memory,
            'storage': _storage,
            'architecture': _architecture,
            'board-name': _board_name,
            'version': _version,
        }

    def __str__(self) -> str:
        return f'{self.identity} ({self.host}) on {self.resources["board-name"]} ({self.resources["architecture"]})'

    def clock_time_get(self) -> time:
        """Returns the router's system time.

        Returns:
            Time with time zone, an instance of the `time` class.

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
        """Returns the router's time zone.

        Returns:
            Time zone in the format Continent/City

        Examples:
            >>> router.clock_time_zone_get()
            'America/Cuiaba'
        """
        return self._get('/system clock get time-zone-name')

    def clock_gmt_offset_get(self) -> str:
        """Returns the router's GMT offset.

        Returns:
            GMT offset in the format +/-HH:MM

        Examples:
            >>> router.clock_gmt_offset_get()
            '-04:00'
        """
        return self._get('/system clock get gmt-offset as-string')

    def clock_dst_active_get(self) -> Optional[bool]:
        """Returns True if DST is enabled, if not enabled, returns False.

        Returns:
            True if DST is enabled, if not enabled, returns False.
        """
        return self._get_bool('/system clock get dst-active')

    def clock_time_zone_autodetect_get(self) -> Optional[bool]:
        """Returns True if time-zone-autodetect is enabled, if not enabled, it returns False.

        Returns:
            True if time-zone-autodetect is enabled,
            if not enabled, returns False.
        """
        return self._get_bool('/system clock get time-zone-autodetect')

    def health_voltage(self) -> float:
        """Returns the current voltage at the router.

        Returns:
            Voltage in Volts

        Examples:
            >>> router.health_voltage()
            24.0
        """
        output = self._get('/system health get number=0 value')
        return float(output)

    def health_temperature(self) -> float:
        """Returns the current temperature at the router.

        Returns:
            Temperature in Celsius

        Examples:
            >>> router.health_temperature()
            40.0
        """
        output = self._get('/system health get number=1 value')
        return float(output)

    def history_system_get(self) -> str:
        """Returns the history of changes made to the router's system settings.

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
        """Sets the router's identity.

        Args:
            new_identity: New identity to be set

        Examples:
            >>> router.identity_set('new_identity')
        """
        new_identity.strip()
        self.cmd(f'/system identity set name={new_identity}')
        self.identity = new_identity

    def note_set(self, note: str, show_at_login: bool = False):
        """Sets the router's note.

        Args:
            note: New note to be set
            show_at_login: Specifies whether a new note should be
                displayed every time a user logs into the router.

        Examples:
            >>> router.note_set('new_note', True)
        """
        show_at_login_command = 'yes' if show_at_login else 'no'
        self.cmd(
            f'/system note set note="{note}" show-at-login={show_at_login_command}'
        )

    def ntp_client_get(
        self,
    ) -> Dict[str, Union[bool, str, int, List[IpAddress], IpAddress]]:
        """Returns the NTP client configuration.

        Returns:
            dict: Dictionary with the NTP client configuration

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
        _enabled = self._get_bool('/system ntp client get enabled')
        _mode = self._get('/system ntp client get mode')
        _servers = self._get_list_ips('/system ntp client get servers')
        _vrf = self._get('/system ntp client get vrf')
        _freq_dift = self._get_number('/system ntp client get freq-drift')
        _status = self._get('/system ntp client get status')
        _synced_server = IpAddress(
            self._get('/system ntp client get synced-server')
        )
        _synced_stratum = self._get_number(
            '/system ntp client get synced-stratum'
        )
        _system_offset = self._get_number(
            '/system ntp client get system-offset'
        )

        return {
            'enabled': _enabled,
            'mode': _mode,
            'servers': _servers,
            'vrf': _vrf,
            'freq-diff': _freq_dift,
            'status': _status,
            'synced-server': _synced_server,
            'synced-stratum': _synced_stratum,
            'system-offset': _system_offset,
        }

    def ntp_client_set(
        self,
        servers: List[IpAddress],
        enabled: bool = True,
        mode: str = 'unicast',
        vrf: str = 'main',
    ):
        """Sets the NTP client configuration.

        Args:
            servers (list): List of NTP servers
            enabled (bool): Specifies whether the NTP client should be enabled
            mode (str): Specifies the NTP client mode
            vrf (str): Specifies the VRF to be used by the NTP client

        Examples:
            >>> router.ntp_client_set(
                '200.160.7.186, 201.49.148.135',
                True,
                'unicast',
                'main'
            )
        """
        servers_command: str = ','.join([str(server) for server in servers])

        enabled_command = 'yes' if enabled else 'no'
        mode = mode.lower().strip()
        if mode not in ['unicast', 'broadcast', 'multicast', 'manycast']:
            raise InvalidNtpMode(f'Invalid mode: {mode}')
        vrf = vrf.lower().strip()

        self.cmd(
            f'/system ntp client set '
            f'enabled={enabled_command} mode={mode} servers={servers_command} vrf={vrf}'
        )

    def ntp_server_get(self) -> dict[str, Union[bool, str, None]]:
        """Returns the NTP server configuration.

        Returns:
            dict: Dictionary with the NTP server configuration

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
            'enabled': boolean(self._get(f'{ntp_command} enabled')),
            'broadcast': boolean(self._get(f'{ntp_command} broadcast')),
            'multicast': boolean(self._get(f'{ntp_command} multicast')),
            'manycast': boolean(self._get(f'{ntp_command} manycast')),
            'broadcast-address': self._get(f'{ntp_command} broadcast-address'),
            'vrf': self._get(f'{ntp_command} vrf'),
        }

    def is_routerboard(self) -> bool:
        """Returns True if the router is a RouterBoard, if not, returns False.

        Returns:
            bool: True if the router is a RouterBoard, if not, returns False
        """
        get_routerboard = self._get('/system routerboard get routerboard')
        if get_routerboard != 'true':
            return False
        return True
