import pytest
from dotenv import load_dotenv
from pydantic import ValidationError

load_dotenv()


@pytest.mark.parametrize(
    ('service', 'default_port'),
    [
        ('api', 8728),
        ('api-ssl', 8729),
        ('ftp', 21),
        ('telnet', 23),
        ('www', 80),
        ('www-ssl', 443),
    ],
)
def test_ip_port_get_command(router, service, default_port):
    assert router.cmd(f'return [/ip service get {service} port]') == str(
        default_port
    )


@pytest.mark.parametrize(
    ('service', 'default_port'),
    [
        ('api', 8728),
        ('api-ssl', 8729),
        ('ftp', 21),
        ('telnet', 23),
        ('www', 80),
        ('www-ssl', 443),
    ],
)
def test_ip_port_get(router, service, default_port):
    assert router.service[service].port == default_port


@pytest.mark.parametrize(
    ('service', 'default_port'),
    [
        ('api', 8728),
        ('api-ssl', 8729),
        ('ftp', 21),
        ('telnet', 23),
        ('www', 80),
        ('www-ssl', 443),
    ],
)
def test_ip_port_set(router, service, default_port):
    router.ip_port_set(service, 65000)
    assert router.service[service].port == 65000  # noqa: PLR2004
    router.ip_port_set(service, default_port)


@pytest.mark.parametrize(
    'service',
    [
        'api',
        'api-ssl',
        'ftp',
        'telnet',
        'www',
        'www-ssl',
    ],
)
def test_ip_port_set_error(router, service):
    with pytest.raises(
        ValidationError, match='Input should be less than or equal to 65535'
    ):
        router.ip_port_set(service, 70000)
