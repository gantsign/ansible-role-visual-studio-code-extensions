Ansible Role: Visual Studio Code Extensions
===========================================

[![Tests](https://github.com/gantsign/ansible-role-visual-studio-code-extensions/workflows/Tests/badge.svg)](https://github.com/gantsign/ansible-role-visual-studio-code-extensions/actions?query=workflow%3ATests)
[![Ansible Galaxy](https://img.shields.io/badge/ansible--galaxy-gantsign.visual--studio--code--extensions-blue.svg)](https://galaxy.ansible.com/gantsign/visual-studio-code-extensions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/gantsign/ansible-role-visual-studio-code-extensions/master/LICENSE)

Role to install extensions for the
[Visual Studio Code](https://code.visualstudio.com) IDE / text editor.

Requirements
------------

* Ansible Core >= 2.12

* OS

    * Linux

      * Debian Family

          * Ubuntu

              * Focal (20.04)
              * Jammy (22.04)

      * RedHat Family

          * Rocky Linux

              * 8

          * Fedora

              * 35

      * SUSE Family

          * openSUSE

              * 15.3

      * Note: other versions are likely to work but have not been tested.

    * macOS

        * Consider macOS support experimental as this time as it's not included
          in the automated tests.

Role Variables
--------------

The following variables will change the behavior of this role (default values
are shown below):

```yaml
# The VS Code build variant:
#   stable   - https://code.visualstudio.com
#   insiders - https://code.visualstudio.com/insiders/
#   oss      - https://github.com/microsoft/vscode/wiki/Differences-between-the-repository-and-Visual-Studio-Code
#              Caution: since Microsoft doesn't distribute binaries for code-oss
#              this role doesn't include tests for code-oss.
#              Note: VSCodium is not presently supported by this role.
visual_studio_code_extensions_build: stable

# Users to install extensions for
users: []
```

Users are configured as follows:

```yaml
users:
  - username: # Unix user name
    # Extensions to be installed if not already present
    visual_studio_code_extensions:
      - # extension 1
      - # extension 2
    # Extensions to be uninstalled if not already absent
    visual_studio_code_extensions_absent:
      - # extension 3
```

Example Playbook
----------------

```yaml
- hosts: servers
  roles:
    - role: gantsign.visual-studio-code-extensions
      users:
        - username: vagrant
          visual_studio_code_extensions:
            - streetsidesoftware.code-spell-checker
            - wholroyd.jinja
            - ms-python.python
          visual_studio_code_extensions_absent:
            - seanmcbreen.Spell
```

More Roles From GantSign
------------------------

You can find more roles from GantSign on
[Ansible Galaxy](https://galaxy.ansible.com/gantsign).

Development & Testing
---------------------

This project uses the following tooling:
* [Molecule](http://molecule.readthedocs.io/) for orchestrating test scenarios
* [Testinfra](http://testinfra.readthedocs.io/) for testing the changes on the
  remote
* [pytest](http://docs.pytest.org/) the testing framework
* [Tox](https://tox.wiki/en/latest/) manages Python virtual
  environments for linting and testing
* [pip-tools](https://github.com/jazzband/pip-tools) for managing dependencies

A Visual Studio Code
[Dev Container](https://code.visualstudio.com/docs/devcontainers/containers) is
provided for developing and testing this role.

License
-------

MIT

Author Information
------------------

John Freeman

GantSign Ltd.
Company No. 06109112 (registered in England)
