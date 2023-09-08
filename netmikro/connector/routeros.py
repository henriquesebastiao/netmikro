from netmiko import ConnectHandler

from netmikro.modules import validate_ip


class RouterOS:
    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        ssh_port: int = 22,
        delay: float = 1,
    ):
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
        self.note = self.connection.send_command('/system note print').split(
            ': '
        )[2]

    def cmd(self, command: str) -> str:
        """
        Sends a command that will be executed on the router
        and returns the output of the command.

        :param command: Command to be executed
        :return: Command output
        """
        return self.connection.send_command(command)

    def get_time(self) -> str:
        output = self.connection.send_command('/system clock print')
        output = output.split(': ')[1]
        return output.split('\n')[0]

    def get_date(self) -> str:
        """Returns the date from the router."""
        output = self.connection.send_command('/system clock print')
        output = output.split(': ')[2]
        return output.split('\n')[0]

    def get_time_zone(self) -> str:
        """Returns the router's time zone."""
        output = self.connection.send_command('/system clock print')
        output = output.split(': ')[4]
        return output.split('\n')[0]

    def get_gmt_offset(self) -> str:
        """Return the router's GMT offset."""
        output = self.connection.send_command('/system clock print')
        output = output.split(': ')[5]
        return output.split('\n')[0]

    def voltage(self) -> float:
        """Returns the router's voltage."""
        output = self.connection.send_command('/system health print')
        output = output.split(' ')
        output = [i for i in output if i != '']
        return float(output[8])

    def temperature(self) -> float:
        """Returns the router's temperature."""
        output = self.connection.send_command('/system health print')
        output = output.split(' ')
        output = [i for i in output if i != '']
        return float(output[12])

    def get_history_system(self) -> str:
        """Returns the router's system history."""
        # TODO: Melhorar como o output e retornado
        output = self.connection.send_command('/system history print')
        return output

    def set_identity(self, new_identity: str):
        """Sets the router's identity."""
        new_identity.strip()
        self.connection.send_command(
            f'/system identity set name={new_identity}'
        )

    # TODO: Implementar métodos para controle de LEDs

    # TODO: Estudar e implementar (logging)

    def set_note(self, note: str, show_at_login: bool = False):
        """
        Sets the router's note.

        :param note: Note to be set
        :param show_at_login: Show note at login
        :return: None
        """
        show_at_login = 'yes' if show_at_login else 'no'
        self.connection.send_command(
            f'/system note set note="{note}" show-at-login={show_at_login}'
        )

    def get_ntp_client(self) -> dict:
        """
        Returns the NTP client configuration.

        :return: Dictionary with NTP client configuration
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

    def set_ntp_client(
        self,
        servers: str,
        enabled: bool = True,
        mode: str = 'unicast',
        vrf: str = 'main',
    ):
        """
        Sets the NTP client configuration.

        :param servers: IP addresses of the NTP servers
        :param enabled: Set NTP client enabled
        :param mode: NTP client mode
        :param vrf: VRF to be used
        :return: None
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
            f'/system ntp client set enabled={enabled} mode={mode} servers={servers} vrf={vrf}'
        )
