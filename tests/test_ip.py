import os

from dotenv import load_dotenv

from ._utils import router

load_dotenv()


def test_api_port_number(router):
    assert router.cmd('return [/ip service get api port]') == '8728'


def test_api_ssl_port_number(router):
    assert router.cmd('return [/ip service get api-ssl port]') == '8729'


def test_ftp_port_number(router):
    assert router.cmd('return [/ip service get ftp port]') == '21'


def test_ssh_port_number(router):
    assert router.cmd('return [/ip service get ssh port]') == os.getenv(
        'SSH_PORT'
    )


def test_telnet_port_number(router):
    assert router.cmd('return [/ip service get telnet port]') == '23'


def test_winbox_port_number(router):
    assert router.cmd('return [/ip service get winbox port]') == os.getenv(
        'WINBOX_PORT'
    )


def test_http_port_number(router):
    assert router.cmd('return [/ip service get www port]') == '80'


def test_https_port_number(router):
    assert router.cmd('return [/ip service get www-ssl port]') == '443'
