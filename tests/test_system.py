from datetime import date, time
from re import match

from netmikro.utils import validate_ip

from ._utils import router


def test_clock_time_get(router):
    assert isinstance(router.clock_time_get(), time)
    assert match(r'\d{2}:\d{2}:\d{2}', router.clock_time_get().isoformat())


def test_clock_date_get(router):
    assert isinstance(router.clock_date_get(), date)
    assert match(r'\d{4}-\d{2}-\d{2}', router.clock_date_get().isoformat())


def test_clock_time_zone_get(router):
    assert router.clock_time_zone_get() == 'America/Cuiaba'


def test_clock_gmt_offset_get(router):
    assert router.clock_gmt_offset_get() == '-04:00'


def test_clock_dst_active_get(router):
    assert isinstance(router.clock_dst_active_get(), bool)


def test_clock_time_zone_autodetect_get(router):
    assert isinstance(router.clock_time_zone_autodetect_get(), bool)


def test_health_voltage(router):
    assert isinstance(router.health_voltage(), float)


def test_health_temperature(router):
    assert isinstance(router.health_temperature(), float)


def test_history_system_get(router):
    assert isinstance(router.history_system_get(), str)


def test_ntp_client_get(router):
    ntp_client_output = router.ntp_client_get()
    assert isinstance(ntp_client_output, dict)
    assert isinstance(ntp_client_output['enabled'], bool)
    for server in ntp_client_output['servers']:
        assert validate_ip(server)
    assert ntp_client_output['vrf'] == 'main'
