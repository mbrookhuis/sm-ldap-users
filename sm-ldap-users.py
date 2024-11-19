#!/usr/bin/env python3
#
# Script: sm-ldap-users.py
#
# Description: mian script
# coding: utf-8

import constants
import smtools
import logger
import ldaptools

def get_existing_users():
    """
    Get the existing users from SUSE Manager Server
    :return:
    """
    log.log_info("get_existing_users")
    smt = smtools.SMTools(log)
    users = smt.get_existing_users()
    del smt
    return users

def get_ldap_users():
    """
    Get the LDAP users from the list of groups
    :return:
    """
    log.log_info("get_ldap_users")
    lt = ldaptools.LDAPTools(log)
    users = lt.get_ldap_users()
    del lt
    return users

def compare_ldap_sm(ldap_users, existing_users):
    """
    Compare the SUSE Manager Users and the LDAP Users.
    - If a user exists in SUMA and not in LDAP, the user will disabled or deleted depending on the setting.
    - If a user exists in SUMA and is also listed in LDAP, check the roles and if the user is enabled. If the roles
      are changed, they will be modified.
    - If a user exists in LDAP and not in SUMA, the user will be created in SUMA.
    :param ldap_users:
    :param existing_users:
    :return:
    """
    log.log_info("compare_ldap_sm")
    users_to_add = []
    changed_users = []
    users_to_delete = []
    users_to_enable = []
    for ldap_user in ldap_users:
        user_changed = False
        user_enable = False
        user_to_be_created = True
        for sm_user in existing_users:
            if ldap_user["login"] == sm_user["login"]:
                user_to_be_created = False
                for role in ldap_user["roles"]:
                    if not role in sm_user["roles"]:
                        user_changed = True
                if not sm_user["enabled"]:
                    user_enable = True
                break
        if user_to_be_created:
            users_to_add.append(ldap_user)
        if user_changed:
            changed_users.append(ldap_user)
        if user_enable:
            users_to_enable.append(ldap_user["login"])
    for sm_user in existing_users:
        delete_user = True
        for ldap_user in ldap_users:
            if ldap_user["login"] == sm_user["login"]:
                delete_user = False
                break
        if delete_user:
            users_to_delete.append(sm_user["login"])
    add_users(users_to_add)
    enable_users(users_to_enable)
    change_users(changed_users)
    delete_users(users_to_delete)
    return

def add_users(users):
    """
    Add the users to SUSE Manager Server
    :param users:
    :return:
    """
    log.log_info("add_users")
    smt = smtools.SMTools(log)
    smt.suman_login()
    for user in users:
        smt.user_create(user['login'], "", user['given_name'], user['last_name'], user['mail'], 1)
        for role in user['roles']:
            smt.user_addrole(user['login'], role)
        log.log_info(f"added user: {user['login']}")
    del smt
    return

def enable_users(users):
    """
    Enable the users on SUSE Manager Server
    :param users:
    :return:
    """
    log.log_info("enable_users")
    smt = smtools.SMTools(log)
    smt.suman_login()
    for user in users:
        smt.user_enable(user)
        log.log_info(f"enabled user: {user}")
    del smt
    return

def change_users(users):
    """
    Change the assigned role of the users on SUSE Manager Server
    :param users:
    :return:
    """
    log.log_info("change_users")
    smt = smtools.SMTools(log)
    smt.suman_login()
    for user in users:
        assigned_roles = smt.user_listroles(user['login'])
        for role in assigned_roles:
            smt.user_removerole(user['login'], role)
        for role in user['roles']:
            smt.user_addrole(user['login'], role)
        log.log_info(f"changed user: {user['login']}")
    del smt
    return

def delete_users(users):
    """
    Delete or disable the users from SUSE Manager Server
    :param users:
    :return:
    """
    log.log_info("delete_users")
    try:
        del_user =  constants.CONFIGSM['delete_user']
    except:
        del_user = False
    smt = smtools.SMTools(log)
    smt.suman_login()
    for user in users:
        if del_user:
            smt.user_delete(user)
            log.log_info(f"deleted user: {user}")
        else:
            assigned_roles = smt.user_listroles(user)
            for role in assigned_roles:
                smt.user_removerole(user, role)
            smt.user_disable(user)
            log.log_info(f"disabled user: {user}")
    del smt
    return

def main():
    """
    Main function
    """
    global log
    try:
        log = logger.Logging()
        log.log_info("Start")
        existing_users = get_existing_users()
        ldap_users = get_ldap_users()
        compare_ldap_sm(ldap_users, existing_users)
    except Exception as err:
        log.log_debug("general error:")
        log.log_debug(err)
        raise
    log.log_info("Completed")

if __name__ == "__main__":
    SystemExit(main())