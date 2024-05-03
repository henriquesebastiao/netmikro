from datetime import date, time
from typing import Dict, List, Optional, Union

from netmikro.exceptions import InvalidNtpMode
from netmikro.modules.base import Base
from netmikro.utils import IpAddress, boolean


# noinspection PyUnresolvedReferences
class System(Base):
    def __init__(self, *args, **kwargs):
        """
        Gets system-related information from the router

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
        super().__init__(*args, **kwargs)

        self.identity = self._get('/system identity get name')

        if self.is_routerboard():
            self.routerboard: dict[str, str] = {
                'model': self._get('/system routerboard get model'),
                'revision': self._get('/system routerboard get revision'),
                'serial-number': self._get(
                    '/system routerboard get serial-number'
                ),
                'firmware-type': self._get(
                    '/system routerboard get firmware-type'
                ),
                'factory-firmware': self._get(
                    '/system routerboard get factory-firmware'
                ),
                'current-firmware': self._get(
                    '/system routerboard get current-firmware'
                ),
                'upgrade-firmware': self._get(
                    '/system routerboard get upgrade-firmware'
                ),
            }

            self.license: dict[str, Union[str, None]] = {
                'software-id': self._get('/system license get software-id'),
                'level': self._get('/system license get nlevel'),
                'features': self._get('/system license get features'),
            }
        else:
            self.license: dict[str, Union[str, None]] = {
                'system-id': self._get('/system license get system-id'),
                'level': self._get('/system license get level'),
            }

        self.note = self._get('/system note get note')

        self.resources: dict[str, Union[str | int]] = {
            'cpu': self._get('/system resources get cpu'),
            'cpu-frequency': int(
                self._get('/system resource get cpu-frequency')
            ),
            'memory': int(self._get('/system resource get total-memory')),
            'storage': int(self._get('/system resource get total-hdd-space')),
            'architecture': self._get(
                '/system resource get architecture-name'
            ),
            'board-name': self._get('/system resource get board-name'),
            'version': self._get('/system resource get version'),
        }

    def __str__(self) -> str:
        return f'{self.identity} ({self.host}) on {self.resources["board-name"]} ({self.resources["architecture"]})'

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
        return self._get('/system clock get gmt-offset as-string')

    def clock_dst_active_get(self) -> Optional[bool]:
        """
        Returns True if DST is enabled, if not enabled, returns False.

        Returns:
            True if DST is enabled, if not enabled, returns False.
        """
        return boolean(self._get('/system clock get dst-active'))

    def clock_time_zone_autodetect_get(self) -> Optional[bool]:
        """
        Returns True if time-zone-autodetect is enabled,
        if not enabled, it returns False.

        Returns:
            True if time-zone-autodetect is enabled,
            if not enabled, returns False.
        """
        return boolean(self._get('/system clock get time-zone-autodetect'))

    def health_voltage(self) -> float:
        """
        Returns the current voltage at the router

        Returns:
            Voltage in Volts

        Examples:
            >>> router.health_voltage()
            24.0
        """
        output = self._get('/system health get number=0 value')
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
        output = self._get('/system health get number=1 value')
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
        self.identity = new_identity

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
            'enabled': boolean(self._get(f'{ntp_command} enabled')),
            'mode': self._get(f'{ntp_command} mode'),
            'servers': servers,
            'vrf': self._get(f'{ntp_command} vrf'),
            'freq-dift': self._get(f'{ntp_command} freq-drift as-string'),
            'status': self._get(f'{ntp_command} status'),
            'synced-server': self._get(f'{ntp_command} synced-server'),
            'synced-stratum': int(self._get(f'{ntp_command} synced-stratum')),
            'system-offset': self._get(
                f'{ntp_command} system-offset as-string'
            ),
        }

    def ntp_client_set(
        self,
        servers: List[IpAddress],
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

        servers: str = ','.join([str(server) for server in servers])

        enabled = 'yes' if enabled else 'no'
        mode = mode.lower().strip()
        if mode not in ['unicast', 'broadcast', 'multicast', 'manycast']:
            raise InvalidNtpMode(f'Invalid mode: {mode}')
        vrf = vrf.lower().strip()

        self.cmd(
            f'/system ntp client set '
            f'enabled={enabled} mode={mode} servers={servers} vrf={vrf}'
        )

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
            'enabled': boolean(self._get(f'{ntp_command} enabled')),
            'broadcast': boolean(self._get(f'{ntp_command} broadcast')),
            'multicast': boolean(self._get(f'{ntp_command} multicast')),
            'manycast': boolean(self._get(f'{ntp_command} manycast')),
            'broadcast-address': self._get(f'{ntp_command} broadcast-address'),
            'vrf': self._get(f'{ntp_command} vrf'),
        }

    def is_routerboard(self) -> bool:
        get_routerboard = self._get('/system routerboard get routerboard')
        if get_routerboard != 'true':
            return False
        return True
