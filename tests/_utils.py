import os
from re import match

from dotenv import load_dotenv
from pytest import fixture

from netmikro.routeros import RouterOS

load_dotenv()


@fixture(scope='session')
def router():
    """Fixture to create a RouterOS connection to be used in tests."""
    connection = RouterOS(
        host=os.getenv('HOST_ROUTER'),
        username=os.getenv('USERNAME_ROUTER'),
        password=os.getenv('PASSWORD_ROUTER'),
        ssh_port=int(os.getenv('SSH_PORT')),
        delay=1,
    )
    yield connection
    connection.disconnect()


@fixture(scope='session')
def chr_router():
    """Fixture to create a RouterOS connection to be used in tests."""
    connection = RouterOS(
        host=os.getenv('HOST_CHR_ROUTER'),
        username=os.getenv('USERNAME_ROUTER'),
        password=os.getenv('PASSWORD_ROUTER'),
        ssh_port=int(os.getenv('SSH_PORT')),
        delay=1,
    )
    yield connection
    connection.disconnect()


@fixture(scope='function')
def clean(router):
    yield ...
    router.identity_set('Netmikro')


def validate_ip(ip):
    """
    Validate if ip is valid

    :param ip: Ip to be validated
    :return: True if ip is valid, False otherwise
    """
    return match(r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$', ip)
