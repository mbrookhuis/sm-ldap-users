#!/usr/bin/env python3
#
# Script: ldaptools.py
#
# Description: This script contains standard function for ldap
#

# coding: utf-8

import constants
from ldap3 import Server, Connection, ALL, SUBTREE

class LDAPTools:
    """
    Class to define needed tools.
    """

    def __init__(self, log):
        self.log = log
        # Connect to the LDAP server
        self.server = Server(constants.CONFIGSM["ldap_uri"], get_info=ALL)
        self.conn = Connection(self.server, constants.CONFIGSM["ldap_default_bind_dn"], constants.CONFIGSM["ldap_password"], auto_bind=True)
        self.search_base = constants.CONFIGSM["ldap_search_base"]

    def __del__(self):
        self.conn.unbind()

    def get_ldap_users(self):
        """
        go to every defined group
          - get the members
          - per member save loginid, role, firstname, lastname and mail-address.
        """
        self.log.log_info("LDAPTools get_ldap_users")
        ldap_users = []
        for group, roles in constants.CONFIGSM["roles"].items():
            assigned_roles = []
            self.log.log_info(roles)
            for role in roles.split(","):
                if role.strip().lower() in constants.SM_ROLES:
                    assigned_roles.append(role.strip().lower())
                else:
                    self.log.log_warning(f"non-existing role {role} defined for group {group}")
            for member in self.get_group_members(group):
                self.conn.search(
                    search_base=member,
                    search_filter='(objectClass=person)',
                    search_scope=SUBTREE,
                    attributes=constants.USER_ATTRIBUTES
                )
                if self.conn.entries:
                    temp_ldap_users = self.add_user_to_found(ldap_users, assigned_roles, self.conn.entries[0])
                    ldap_users = temp_ldap_users
                else:
                    self.log.log_warning(f"Details for {member} could not be found.")
        return ldap_users

    def get_group_members(self, group):
        """
        Get the users assigned to the group
        :param group:
        :return:
        """
        self.conn.search(
            search_base=self.search_base,
            search_filter=f'(&(objectClass=group)(cn={group}))',
            search_scope=SUBTREE,
            attributes=['member']  # Modify based on your LDAP schema
        )
        if self.conn.entries:
            group_entry = self.conn.entries[0]
            return group_entry.member.values if 'member' in group_entry else []
        return ""

    def add_user_to_found(self, ldap_users, roles, details):
        """
        Combine the found users and the assigned role. Also check that every user only is listed once
        and that the roles are unique too.
        :param ldap_users:
        :param roles:
        :param details:
        :return:
        """
        need_to_add = True
        temp = ldap_users
        for ldap_user in temp:
            if ldap_user["login"].strip().lower() == details.sAMAccountName.value.strip().lower():
                need_to_add = False
                for role in roles:
                    if not role in ldap_user["roles"]:
                        ldap_user["roles"].append(role)
                break
        if need_to_add:
            add_user = {"login": details.sAMAccountName.value, "roles": roles}
            if details.givenName.value:
                add_user["given_name"] = details.givenName.value
            else:
                add_user["given_name"] = details.sAMAccountName.value
            if details.sn.value:
                add_user["last_name"] = details.sn.value
            else:
                add_user["last_name"] = details.sAMAccountName.value
            if details.mail.value:
                add_user["mail"] = details.mail.value
            else:
                add_user["mail"] = constants.CONFIGSM["default_user_mail"]
            temp.append(add_user)
        return temp
