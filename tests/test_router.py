from ._utils import router


def test_cmd(router):
    assert router.cmd('/system identity print') == 'name: Netmikro'


def test_cmd_multilines(router):
    output = router.cmd_multiline(
        ['return [system/identity/get name]', 'return [system/note/get note]']
    )

    assert 'Netmikro' in output
    assert 'Test note' in output


def test_identity(router):
    assert router.identity == 'Netmikro'
