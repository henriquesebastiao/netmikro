from netmikro import RouterOS
from re import match

router = RouterOS('192.168.3.3', 'test', 'test', 22)


def test_routeros_cmd():
    assert router.cmd('/system identity print') == 'name: test'


def test_routeros_system_get_time():
    assert match(r'\d{2}:\d{2}:\d{2}', router.get_time())


def test_routeros_system_get_date():
    assert match(r'\d{4}-\d{2}-\d{2}', router.get_date())


def test_get_time_zone():
    assert router.get_time_zone() == 'America/Cuiaba'


def test_routeros_system_get_gmt_offset():
    assert router.get_gmt_offset() == '-04:00'


def test_routeros_system_get_voltage():
    assert 20 < router.voltage() < 30


def test_routeros_system_get_temperature():
    assert isinstance(router.temperature(), float)


def test_routeros_system_get_history_system():
    assert isinstance(router.get_history_system(), str)


def test_routeros_system_get_identity():
    assert router.identity == 'test'


def test_routeros_system_get_identity_fail():
    assert router.identity != 'test_fail'
