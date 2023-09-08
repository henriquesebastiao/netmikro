from re import match

from netmikro import RouterOS
from netmikro.modules import validate_ip

router = RouterOS('192.168.3.3', 'test', 'test', 22, 1)


def test_routeros_cmd():
    assert router.cmd('/system identity print') == 'name: test'


def test_clock_time_get():
    assert match(r'\d{2}:\d{2}:\d{2}', router.clock_time_get())


def test_clock_date_get():
    assert match(r'\d{4}-\d{2}-\d{2}', router.clock_date_get())


def test_clock_time_zone_get():
    assert router.clock_time_zone_get() == 'America/Cuiaba'


def test_clock_gmt_offset_get():
    assert router.clock_gmt_offset_get() == '-04:00'


def test_clock_dst_active_get():
    assert isinstance(router.clock_dst_active_get(), bool)


def test_clock_time_zone_autodetect_get():
    assert isinstance(router.clock_time_zone_autodetect_get(), bool)


def test_health_voltage():
    assert 20 < router.health_voltage() < 30


def test_health_temperature():
    assert isinstance(router.health_temperature(), float)


def test_history_system_get():
    assert isinstance(router.history_system_get(), str)


def test_identity():
    assert router.identity == 'test'


def test_identity_fail():
    assert router.identity != 'test_fail'


def test_ntp_client_get():
    ntp_client_output = router.ntp_client_get()
    assert isinstance(ntp_client_output['enabled'], bool)
    for server in ntp_client_output['servers']:
        assert validate_ip(server)
    assert ntp_client_output['vrf'] == 'main'
