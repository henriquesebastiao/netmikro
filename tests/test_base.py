from dotenv import load_dotenv

from tests._utils import router

load_dotenv()


def test_base_get_number_return_0_if_output_is_empty(router):
    assert router._get_number('/system/license/get features') == 0


def test_base_get_float_return_0_if_output_is_empty(router):
    assert router._get_float('/system/license/get features') == 0.0
