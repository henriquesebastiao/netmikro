from re import match

from netmikro.exceptions import InvalidIpAddress


# noinspection PyUnresolvedReferences
class IpAddress:
    """Class that represents an IP address.

    Args:
        address (str): The IP address to be represented.

    Attributes:
        address (str): The IP address.
        binary (str): The IP address in binary format.
        class_address (str): The class of the IP address.
        addresses_on_network (int): The number of addresses on the network.
        address_type (str): The type of the IP address.

    Methods:
        __str__: Returns the IP address.
        __repr__: Returns the representation of the class.
        __eq__: Compares two IP addresses.

    Examples:
        >>> ip = IpAddress('192.168.88.1')
        >>> ip.address
        '192.168.88.1'
        >>> ip.binary
        '11000000.10101000.01011000.00000001'
        >>> ip.class_address
        'C'
        >>> ip.addresses_on_network
        256
        >>> ip.address_type
        'PRIVATE'
    """

    def __init__(self, address: str):
        if not match(r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$', address):
            raise InvalidIpAddress(f'Invalid IP address: {address}')

        octets: list[int] = [int(part) for part in address.split('.')]

        self.address = address
        self.binary = '.'.join([format(int(octet), '08b') for octet in octets])

        class_ranges = {
            'A': (range(0, 128), 2**24),
            'B': (range(128, 192), 2**16),
            'C': (range(192, 224), 2**8),
            'D': (range(224, 240), None),
            'E': (range(240, 256), None),
        }

        for class_address, (
            range_ip,
            addresses_on_network,
        ) in class_ranges.items():
            if octets[0] in range_ip:
                self.class_address = class_address
                self.addresses_on_network = addresses_on_network
                break

        self.address_type = self.address_type_check(octets)

    def __str__(self) -> str:
        return self.address

    def __repr__(self):
        return f'IpAddress(address="{self.address}")'

    def __eq__(self, other):
        return self.address == other.address

    @classmethod
    def address_type_check(cls, octets: list[int]) -> str:
        """Get the type of IP address.

        Args:
            octets (list): List of integers representing the IP address.

        Returns:
            str: The type of the IP address.

        Examples:
            >>> IpAddress.address_type_check([192, 168, 88, 1])
            'PRIVATE'
        """
        address_types = {
            (0,): 'CURRENT',
            (10,): 'PRIVATE',
            (172, 16): 'PRIVATE',
            (192, 168): 'PRIVATE',
            (14,): 'PUBLIC',
            (39,): 'RESERVED',
            (127,): 'LOCALHOST',
            (128,): 'RESERVED (IANA)',
            (169, 254): 'ZEROCONF',
            (191, 255): 'RESERVED (IANA)',
            (192, 0, 2): 'DOCUMENTATION',
            (192, 88, 99): 'IPv6 to IPv4',
            (198, 18): 'TEST-NET',
            (223, 255, 255): 'RESERVED',
            (224,): 'MULTICAST',
            (240,): 'RESERVED',
            (255,): 'BROADCAST',
        }

        for address_type, address_value in address_types.items():
            if octets[: len(address_type)] == list(address_type):
                return address_value

        return 'UNKNOWN'
