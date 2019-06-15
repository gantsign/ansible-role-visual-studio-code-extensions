import pytest
import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('extension', [
    'ms-python.python',
    'wholroyd.jinja'
])
def test_visual_studio_code(host, extension):
    output = host.check_output('sudo --user test_usr -H code %s %s',
                               '--install-extension', extension)
    assert 'already installed' in output


def test_visual_studio_code_extensions(host):
    output = host.check_output('sudo --user test_usr -H code %s',
                               '--list-extensions')
    assert 'ms-python.python' in output


def test_visual_studio_code_uninstall_extensions(host):
    output = host.check_output('sudo --user test_usr -H code %s',
                               '--list-extensions')
    assert 'seanmcbreen.Spell' not in output


@pytest.mark.parametrize('extension', [
    'ms-python.python',
    'wholroyd.jinja'
])
def test_visual_studio_code_insiders(host, extension):
    output = host.check_output('sudo --user test_usr -H code-insiders %s %s',
                               '--install-extension', extension)
    assert 'already installed' in output


def test_visual_studio_code_extensions_insiders(host):
    output = host.check_output('sudo --user test_usr -H code-insiders %s',
                               '--list-extensions')
    assert 'ms-python.python' in output


def test_visual_studio_code_uninstall_extensions_insiders(host):
    output = host.check_output('sudo --user test_usr -H code-insiders %s',
                               '--list-extensions')
    assert 'seanmcbreen.Spell' not in output
