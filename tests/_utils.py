import os

from pytest import fixture

from netmikro.connector.routeros import RouterOS


@fixture(scope='session')
def router():
    """Fixture to create a RouterOS connection to be used in tests."""
    connection = RouterOS(
        host=os.getenv('HOST'),
        username=os.getenv('USERNAME'),
        password=os.getenv('PASSWORD'),
        ssh_port=int(os.getenv('SSH_PORT')),
        delay=1,
    )
    yield connection
    connection.disconnect()


@fixture(scope='function')
def clean(router):
    yield ...
    router.identity_set('Netmikro')
