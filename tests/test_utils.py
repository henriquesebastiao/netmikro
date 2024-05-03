import pytest

from netmikro.exceptions import UndefinedBooleanValue
from netmikro.utils import boolean
from netmikro.utils.common import InvalidIpAddress, IpAddress
from tests._utils import ip


def test_ip_address_class_invalid_ip():
    with pytest.raises(
        InvalidIpAddress, match='Invalid IP address: 999.999.999.999'
    ):
        IpAddress('999.999.999.999')


def test_ip_address_class_representation(ip):
    assert str(ip) == '1.1.1.1'


def test_ip_address_repr(ip):
    assert repr(ip) == f'IpAddress(address="{ip}")'


def test_ip_address_eq():
    ip = '1.1.1.1'
    ip_instance = IpAddress(ip)
    assert ip_instance == IpAddress(ip)


def test_ip_address_class_type_checker():
    assert IpAddress.address_type_check([10, 0, 0, 0]) == 'PRIVATE'


def test_convert_to_boolean():
    assert boolean('true')
    assert boolean('false') is False
    assert boolean('') is None

    with pytest.raises(
        UndefinedBooleanValue, match='Undefined boolean value: test'
    ):
        boolean('test')
