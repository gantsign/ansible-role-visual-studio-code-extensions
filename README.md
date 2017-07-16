Ansible Role: Visual Studio Code Extensions
===========================================

[![Build Status](https://travis-ci.org/gantsign/ansible-role-visual-studio-code-extensions.svg?branch=master)](https://travis-ci.org/gantsign/ansible-role-visual-studio-code-extensions)
[![Ansible Galaxy](https://img.shields.io/badge/ansible--galaxy-gantsign.visual--studio--code--extensions-blue.svg)](https://galaxy.ansible.com/gantsign/visual-studio-code-extensions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/gantsign/ansible-role-visual-studio-code-extensions/master/LICENSE)

Role to install extensions for the
[Visual Studio Code](https://code.visualstudio.com) IDE / text editor.

Requirements
------------

* Ansible >= 2.0

* OS

    * Linux

      * Debian Family

          * Ubuntu

              * Xenial (16.04)

      * SUSE Family

          * OpenSUSE

              * 42.2

      * Note: other versions are likely to work but have not been tested.

    * MacOSX

        * Consider MacOSX support experimental as this time as it's not included
          in the automated tests.

Role Variables
--------------

The following variables will change the behavior of this role (default values
are shown below):

```yaml
# The name of the group for user files and folders (leave as null to use default
# value). Defaults to `users` on SUSE, `admin` on MacOSX and the username on all
# other OSs / distributions.
visual_studio_code_extensions_user_group_name: null

# Users to install extensions for
users: []

# List of extensions to be uninstalled for a particular user
# Defaults to empty list
# value can be specified as shown below
# visual_studio_code_extensions_absent: 
#   - ms-vscode.csharp
visual_studio_code_extensions_absent: []
```

Users are configured as follows:

```yaml
users:
  - username: # Unix user name
    visual_studio_code_extensions:
      - # extension 1
      - # extension 2
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
            - donjayamanne.python
          visual_studio_code_extensions_absent:
            - streetsidesoftware.code-spell-checker
```

More Roles From GantSign
------------------------

You can find more roles from GantSign on
[Ansible Galaxy](https://galaxy.ansible.com/gantsign).

Development & Testing
---------------------

This project uses [Molecule](http://molecule.readthedocs.io/) to aid in the
development and testing; the role is unit tested using
[Testinfra](http://testinfra.readthedocs.io/) and
[pytest](http://docs.pytest.org/).

To develop or test you'll need to have installed the following:

* Linux (e.g. [Ubuntu](http://www.ubuntu.com/))
* [Docker](https://www.docker.com/)
* [Python](https://www.python.org/) (including python-pip)
* [Ansible](https://www.ansible.com/)
* [Molecule](http://molecule.readthedocs.io/)

To run the role (i.e. the `tests/test.yml` playbook), and test the results
(`tests/test_role.py`), execute the following command from the project root
(i.e. the directory with `molecule.yml` in it):

```bash
molecule test
```

License
-------

MIT

Author Information
------------------

John Freeman

GantSign Ltd.
Company No. 06109112 (registered in England)
