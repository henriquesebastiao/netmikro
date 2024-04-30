import os

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


@fixture(scope='function')
def clean(router):
    yield ...
    router.identity_set('Netmikro')
