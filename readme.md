# Tool to create users in SUSE Manager Server based on LDAP groups

## Overview
This tool is used to create users in SUSE Manager Server based on LDAP/AD groups. For each LDAP/AD group a role within SUSE Manager Server is defined. 
Also, the tool will check if existing users still have the role they should have, and, if not, it will be corrected. The same for if a user is disabled, it will be enabled again.
If a users is not present in the LDAP/AD groups anymore, it will be disabled or deleted, depending on the configuration.

The code is writen for Python 3.6 (the default with SLES15.x), but will also work with newer versions.

## Table of contents
- [Installation](#installation)
- [Usage](#usage)

## Installation
To install this project, perform the following steps:
- Be sure that python 3.6 is installed and also the module python3-PyYAML. Also the ldap3 module is needed:
```bash
zypper in python3 python3-PyYAML
pip install yaml
- ```
- On the server or PC, where it should run, create a directory. On linux, e.g. /opt/sm-ldap-users
- Copy all the file to this directory.
- Edit the configsm.yaml. All parameters should be entered. Tip: for the ldap information, the best would be to use the same as for SSSD.
- Be sure that the file sm-ldap-users.py is executable. It would be good to change the owner to root:root and only root can read and execute:
```bash
chmod 600 * 
chmod 700 sm-ldap-users.py
chown root:root * 
- ```

## Usage
This is very simple. Once the configsm.yaml contains the correct information, executing the following will do the magic:
```bash
<dir>/sm-ldap-users.py
```


