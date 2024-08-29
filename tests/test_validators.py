import pytest
from pydantic import ValidationError

from netmikro import RouterOS
from netmikro.exceptions import UndefinedBooleanValue
from netmikro.utils import boolean


def test_convert_to_boolean():
    assert boolean('true')
    assert boolean('false') is False
    assert boolean('') is None

    with pytest.raises(
        UndefinedBooleanValue, match='Undefined boolean value: test'
    ):
        boolean('test')


def test_create_connection_with_str_port():
    with pytest.raises(
        ValidationError,
        match='Input should be a valid integer, unable to parse string as an integer',
    ):
        RouterOS(
            host='192.168.3.4',
            username='netmikro',
            password='nulliusinverba',
            ssh_port='sdews',
        )


def test_create_connection_with_negative_port():
    with pytest.raises(
        ValidationError, match='Input should be greater than or equal to 0'
    ):
        RouterOS(
            host='192.168.3.4',
            username='netmikro',
            password='nulliusinverba',
            ssh_port=-1,
        )


def test_create_connection_with_very_bic_port():
    with pytest.raises(
        ValidationError, match='Input should be less than or equal to 65535'
    ):
        RouterOS(
            host='192.168.3.4',
            username='netmikro',
            password='nulliusinverba',
            ssh_port=80000,
        )
