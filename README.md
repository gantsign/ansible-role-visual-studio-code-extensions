Ansible Role: Visual Studio Code Extensions
===========================================

[![Build Status](https://travis-ci.org/gantsign/ansible-role-visual-studio-code-extensions.svg?branch=master)](https://travis-ci.org/gantsign/ansible-role-visual-studio-code-extensions)
[![Ansible Galaxy](https://img.shields.io/badge/ansible--galaxy-gantsign.visual--studio--code--extensions-blue.svg)](https://galaxy.ansible.com/gantsign/visual-studio-code-extensions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/gantsign/ansible-role-visual-studio-code-extensions/master/LICENSE)

Role to install extensions for the
[Visual Studio Code](https://code.visualstudio.com) IDE / text editor.

Requirements
------------

* Ansible >= 2.4

* OS

    * Linux

      * Debian Family

          * Ubuntu

              * Xenial (16.04)

      * RedHat Family

          * CentOS

              * 7

          * Fedora

              * 27

      * SUSE Family

          * OpenSUSE

              * 42.2

      * Note: other versions are likely to work but have not been tested.

    * macOS

        * Consider macOS support experimental as this time as it's not included
          in the automated tests.

Role Variables
--------------

The following variables will change the behavior of this role (default values
are shown below):

```yaml
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

To test this role run the following command from the project root:

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
