import pytest

from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')


@pytest.mark.parametrize('extension', [
    'ms-python.python',
    'wholroyd.jinja'
])
def test_visual_studio_code(Command, extension):
    output = Command.check_output('sudo --user test_usr -H code %s %s',
                                  '--install-extension', extension)
    assert 'already installed' in output


def test_visual_studio_code_extensions(Command):
    output = Command.check_output('sudo --user test_usr -H code %s',
                                  '--list-extensions')
    assert 'ms-python.python' in output


def test_visual_studio_code_uninstall_extensions(Command):
    output = Command.check_output('sudo --user test_usr -H code %s',
                                  '--list-extensions')
    assert 'seanmcbreen.Spell' not in output
