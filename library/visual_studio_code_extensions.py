#!/usr/bin/python

# Make coding more python3-ish
from __future__ import absolute_import, division, print_function

import os

from ansible.module_utils.basic import AnsibleModule

__metaclass__ = type


def is_extension_installed(module, executable, executable_args, name):
    rc, stdout, stderr = module.run_command(
        [executable] + executable_args + ['--list-extensions', name])
    if rc != 0 or stderr:
        module.fail_json(
            msg=(f'Error querying installed extensions [{name}]: '
                 f'{stdout + stderr }'))
    lowername = name.lower()
    match = next((x for x in stdout.splitlines()
                 if x.lower() == lowername), None)
    return match is not None


def list_extension_dirs(executable, executable_args):
    dirname = '.vscode'
    if executable == 'code-insiders':
        dirname += '-insiders'
    if executable == 'code-oss':
        dirname += '-oss'


    if executable == 'flatpak' and 'com.vscodium.codium' in executable_args:
        ext_dir = os.path.expanduser(
            os.path.join('~', '.var', 'app', 'com.vscodium.codium', 'data', 'codium', 'extensions'))
    else:
        ext_dir = os.path.expanduser(
            os.path.join('~', dirname, 'extensions'))

    ext_dirs = sorted([f for f in os.listdir(
        ext_dir) if os.path.isdir(os.path.join(ext_dir, f))])
    return ext_dirs


def install_extension(module, executable, executable_args, name):
    if is_extension_installed(module, executable, executable_args, name):
        # Use the fact that extension directories names contain the version
        # number
        before_ext_dirs = list_extension_dirs(executable, executable_args)
        # Unfortunately `--force` suppresses errors (such as extension not
        # found)
        rc, stdout, stderr = module.run_command(
            [executable] + executable_args + ['--install-extension', name, '--force'])
        # Whitelist: [DEP0005] DeprecationWarning: Buffer() is deprecated due
        # to security and usability issues.
        if rc != 0 or (stderr and '[DEP0005]' not in stderr):
            module.fail_json(
                msg=(f'Error while upgrading extension [{name}]: '
                     f'({rc}) {stdout + stderr}'))
        after_ext_dirs = list_extension_dirs(executable, executable_args)
        changed = before_ext_dirs != after_ext_dirs
        return changed, 'upgrade'
    else:
        rc, stdout, stderr = module.run_command(
            [executable] + executable_args + ['--install-extension', name])
        # Whitelist: [DEP0005] DeprecationWarning: Buffer() is deprecated due
        # to security and usability issues.
        if rc != 0 or (stderr and '[DEP0005]' not in stderr):
            module.fail_json(
                msg=(f'Error while installing extension [{name}]: '
                     f'({rc}) {stdout + stderr}'))
        changed = 'already installed' not in stdout
        return changed, 'install'


def uninstall_extension(module, executable, executable_args, name):
    if is_extension_installed(module, executable, executable_args, name):
        rc, stdout, stderr = module.run_command(
            [executable] + executable_args + ['--uninstall-extension', name])
        if 'successfully uninstalled' not in (stdout + stderr):
            module.fail_json(
                msg=((f'Error while uninstalling extension [{name}] '
                     f'unexpected response: {stdout + stderr}')))
        return True
    return False


def run_module():

    module_args = dict(
        executable=dict(
            type='str',
            required=False,
            choices=[
                'code',
                'code-insiders',
                'code-oss',
                'flatpak'],
            default='code'),
        executable_args=dict(
            elements='str',
            type='list',
            required=False,
            default=[]),
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
    if executable not in ['code-insiders', 'code-oss', 'flatpak']:
        executable = 'code'

    executable_args = module.params['executable_args']

    name = module.params['name']
    state = module.params['state']

    if state == 'absent':
        changed = uninstall_extension(module, executable, executable_args, name)

        if changed:
            msg = f'{name} is now uninstalled'
        else:
            msg = f'{name} is not installed'
    else:
        changed, change = install_extension(module, executable, executable_args, name)

        if changed:
            if change == 'upgrade':
                msg = f'{name} was upgraded'
            else:
                msg = f'{name} is now installed'
        else:
            msg = f'{name} is already installed'

    module.exit_json(changed=changed, msg=msg)


def main():
    run_module()


if __name__ == '__main__':
    main()
