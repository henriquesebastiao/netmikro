import os
from datetime import date, time
from re import match

import pytest

from netmikro.exceptions import InvalidNtpMode
from netmikro.utils import boolean
from tests._utils import chr_router, router, validate_ip


def test_system_str(router):
    identity = os.getenv('IDENTITY')
    host = os.getenv('HOST_ROUTER')
    board_name = os.getenv('BOARD_NAME')
    architecture = os.getenv('ARCHITECTURE')
    assert (
        str(router) == f'{identity} ({host}) on {board_name} ({architecture})'
    )


def test_system_clock_time_get(router):
    assert isinstance(router.clock_time_get(), time)
    assert match(r'\d{2}:\d{2}:\d{2}', router.clock_time_get().isoformat())


def test_system_clock_date_get(router):
    assert isinstance(router.clock_date_get(), date)
    assert match(r'\d{4}-\d{2}-\d{2}', router.clock_date_get().isoformat())


def test_system_clock_time_zone_get(router):
    assert router.clock_time_zone_get() == 'America/Cuiaba'


def test_system_clock_gmt_offset_get(router):
    assert router.clock_gmt_offset_get() == '-04:00'


def test_system_clock_dst_active_get(router):
    assert isinstance(router.clock_dst_active_get(), bool)


def test_system_clock_time_zone_autodetect_get(router):
    assert isinstance(router.clock_time_zone_autodetect_get(), bool)


def test_system_health_voltage(router):
    assert isinstance(router.health_voltage(), float)


def test_system_health_temperature(router):
    assert isinstance(router.health_temperature(), float)


def test_system_history_system_get(router):
    assert isinstance(router.history_system_get(), str)


def test_system_identity(router):
    assert router.identity == os.getenv('IDENTITY')


def test_system_identity_set(router):
    new_identity = 'test'
    router.identity_set(new_identity)
    assert router.identity == new_identity
    assert router.identity != os.getenv('IDENTITY')
    router.identity_set(os.getenv('IDENTITY'))


def test_system_license(router):
    assert isinstance(router.license, dict)
    assert router.license['software-id'] == os.getenv('SYSTEM_ID_ROUTER')
    assert router.license['level'] == int(os.getenv('LEVEL_ROUTER'))


def test_system_ntp_client_get(router):
    ntp_client_output = router.ntp_client_get()
    assert isinstance(ntp_client_output, dict)
    assert isinstance(ntp_client_output['enabled'], bool)
    assert ntp_client_output['vrf'] == 'main'


def test_system_ntp_client_set(router):
    servers = ['200.186.125.195', '200.20.186.76']
    router.ntp_client_set(servers=servers)
    set_servers = router._get('/system ntp client get servers').split(';')
    for server in servers:
        assert server in set_servers
    router.ntp_client_set(servers=['200.160.7.186', '201.49.148.135'])

    with pytest.raises(InvalidNtpMode, match='Invalid mode: test'):
        router.ntp_client_set(
            servers=['200.186.125.195', '200.20.186.76'], mode='test'
        )


def test_system_ntp_server_get(router):
    ntp_server_output = router.ntp_server_get()
    assert isinstance(ntp_server_output, dict)
    assert isinstance(ntp_server_output['enabled'], bool)
    assert isinstance(ntp_server_output['broadcast'], bool)
    assert isinstance(ntp_server_output['multicast'], bool)
    assert isinstance(ntp_server_output['manycast'], bool)
    assert ntp_server_output['vrf'] == 'main'


def test_system_note_set(router):
    test_string = 'test test'
    router.note_set(note=test_string, show_at_login=True)
    assert router._get('/system note get note') == test_string
    assert boolean(router._get('/system note get show-at-login'))
    router.note_set(note=os.getenv('NOTE'), show_at_login=False)


def test_system_is_routerboard_false(chr_router):
    assert not chr_router.is_routerboard()
