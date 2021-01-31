import pytest


@pytest.mark.parametrize('extension', [
    'EditorConfig.EditorConfig',
    'wholroyd.jinja'
])
def test_visual_studio_code(host, extension):
    output = host.check_output('sudo --user test_usr -H code %s %s',
                               '--install-extension', extension)
    assert 'already installed' in output


def test_visual_studio_code_extensions(host):
    output = host.check_output('sudo --user test_usr -H code %s',
                               '--list-extensions')
    assert 'EditorConfig.EditorConfig' in output


def test_visual_studio_code_uninstall_extensions(host):
    output = host.check_output('sudo --user test_usr -H code %s',
                               '--list-extensions')
    assert 'seanmcbreen.Spell' not in output


@pytest.mark.parametrize('extension', [
    'EditorConfig.EditorConfig',
    'wholroyd.jinja'
])
def test_visual_studio_code_insiders(host, extension):
    output = host.check_output('sudo --user test_usr -H code-insiders %s %s',
                               '--install-extension', extension)
    assert 'already installed' in output


def test_visual_studio_code_extensions_insiders(host):
    output = host.check_output('sudo --user test_usr -H code-insiders %s',
                               '--list-extensions')
    assert 'EditorConfig.EditorConfig' in output


def test_visual_studio_code_uninstall_extensions_insiders(host):
    output = host.check_output('sudo --user test_usr -H code-insiders %s',
                               '--list-extensions')
    assert 'seanmcbreen.Spell' not in output
