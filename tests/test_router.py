import os

from dotenv import load_dotenv

from ._utils import router

load_dotenv()


def test_cmd(router):
    assert router.cmd('/system identity print') == 'name: ' + os.getenv(
        'IDENTITY'
    )


def test_cmd_multilines(router):
    output = router.cmd_multiline(
        [
            'return [/system identity get name]',
            'return [/system note get note]',
        ]
    )

    assert router.identity in output
    assert 'Test note' in output


def test_identity(router):
    assert router.identity == os.getenv('IDENTITY')
