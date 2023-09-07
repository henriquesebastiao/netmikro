from netmiko import ConnectHandler


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
        output = self.connection.send_command('/system health print')
        output = output.split(' ')
        output = [i for i in output if i != '']
        return float(output[8])

    def temperature(self) -> float:
        output = self.connection.send_command('/system health print')
        output = output.split(' ')
        output = [i for i in output if i != '']
        return float(output[12])

    def get_history_system(self):
        # TODO: Melhorar como o output e retornado
        output = self.connection.send_command('/system history print')
        return output

    def set_identity(self, new_identity: str):
        new_identity.strip()
        self.connection.send_command(
            f'/system identity set name={new_identity}'
        )
