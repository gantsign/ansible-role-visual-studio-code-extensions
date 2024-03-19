#!/usr/bin/python

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function

import os

from ansible.module_utils.basic import AnsibleModule

__metaclass__ = type


def is_extension_installed(module, executable, name):
    rc, stdout, stderr = module.run_command(
        [executable, '--list-extensions', name])
    if rc != 0:
        module.fail_json(
            msg=f'Error querying installed extensions [{name}]',
                rc=rc, stdout=stdout, stderr=stderr)
    lowername = name.lower()
    match = next((x for x in stdout.splitlines()
                 if x.lower() == lowername), None)
    return match is not None, stdout, stderr


def list_extension_dirs(executable):
    dirname = '.vscode'
    if executable == 'code-insiders':
        dirname += '-insiders'
    if executable == 'code-oss':
        dirname += '-oss'

    ext_dir = os.path.expanduser(
        os.path.join('~', dirname, 'extensions'))

    ext_dirs = sorted([f for f in os.listdir(
        ext_dir) if os.path.isdir(os.path.join(ext_dir, f))])
    return ext_dirs


def install_extension(module, executable, name):
    installed, installed_stdout, installed_stderr = is_extension_installed(module, executable, name)
    if installed:
        # Use the fact that extension directories names contain the version
        # number
        before_ext_dirs = list_extension_dirs(executable)
        # Unfortunately `--force` suppresses errors (such as extension not
        # found)
        rc, stdout, stderr = module.run_command(
            [executable, '--install-extension', name, '--force'])
        if rc != 0:
            module.fail_json(
                msg=f'Error while upgrading extension [{name}]',
                    rc=rc, stdout=installed_stdout+stdout, stderr=installed_stderr+stderr)
        after_ext_dirs = list_extension_dirs(executable)
        changed = before_ext_dirs != after_ext_dirs
        if installed_stderr == stderr:
            installed_stderr = ''
        return changed, 'upgrade', installed_stdout+stdout, installed_stderr+stderr
    else:
        rc, stdout, stderr = module.run_command(
            [executable, '--install-extension', name])
        if rc != 0:
            module.fail_json(
                msg=f'Error while installing extension [{name}]',
                    rc=rc, stdout=installed_stdout+stdout, stderr=installed_stderr+stderr)
        changed = 'already installed' not in stdout
        if installed_stderr == stderr:
            installed_stderr = ''
        return changed, 'install', installed_stderr+stderr


def uninstall_extension(module, executable, name):
    installed, installed_stdout, installed_stderr = is_extension_installed(module, executable, name)
    if installed:
        rc, stdout, stderr = module.run_command(
            [executable, '--uninstall-extension', name])
        if rc != 0:
            module.fail_json(
                msg=f'Error while uninstalling extension [{name}]',
                    rc=rc, stdout=installed_stdout+stdout, stderr=installed_stderr+stderr)
        if installed_stderr == stderr:
            installed_stderr = ''
        return True, installed_stdout+stdout, installed_stderr+stderr
    return False, installed_stdout, installed_stderr


def run_module():

    module_args = dict(
        executable=dict(
            type='str',
            required=False,
            choices=[
                'code',
                'code-insiders',
                'code-oss'],
            default='code'),
        name=dict(
            type='str',
            required=True),
        state=dict(
            type='str',
            default='present',
            choices=[
                'absent',
                'present']))

    module = AnsibleModule(argument_spec=module_args,
                           supports_check_mode=False)

    executable = module.params['executable']
    if executable != 'code-insiders' and executable != 'code-oss':
        executable = 'code'

    name = module.params['name']
    state = module.params['state']

    if state == 'absent':
        changed, stdout, stderr = uninstall_extension(module, executable, name)

        if changed:
            msg = f'{name} is now uninstalled'
        else:
            msg = f'{name} is not installed'
    else:
        changed, change, stdout, stderr = install_extension(module, executable, name)

        if changed:
            if change == 'upgrade':
                msg = f'{name} was upgraded'
            else:
                msg = f'{name} is now installed'
        else:
            msg = f'{name} is already installed'

    module.exit_json(changed=changed, msg=msg, stdout=stdout, stderr=stderr)


def main():
    run_module()


if __name__ == '__main__':
    main()
