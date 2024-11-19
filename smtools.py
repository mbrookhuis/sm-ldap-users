#!/usr/bin/env python3
#
# Script: smtools.py
#
# Description: This script contains standard function for SUSE Manager
#

# coding: utf-8


import xmlrpc.client
import socket
import constants

class SMTools:
    """
    Class to define needed tools.
    """
    client = ""
    session = ""
    sid = ""

    def __init__(self, log):
        self.log = log

    def __del__(self):
        self.suman_logout()

    def suman_login(self):
        """
        Log in to SUSE Manager Server.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect_ex((constants.CONFIGSM['suma_server'], 443))
        except:
            self.log.fatal_error("Unable to login to SUSE Manager server {}".format(constants.CONFIGSM['suma_server']))

        self.client = xmlrpc.client.Server("https://" + constants.CONFIGSM['suma_server'] + "/rpc/api")
        try:
            self.session = self.client.auth.login(constants.CONFIGSM['suma_user'], constants.CONFIGSM['suma_password'])
        except xmlrpc.client.Fault:
            self.log.fatal_error("Unable to login to SUSE Manager server {}".format(constants.CONFIGSM['suma_server']))

    def suman_logout(self):
        """
        Logout from SUSE Manager Server.
        """
        try:
            self.client.auth.logout(self.session)
        except xmlrpc.client.Fault:
            self.log.log_error("Unable to logout from SUSE Manager {}".format(constants.CONFIGSM['suma_server']))

    def user_listusers(self):
        """
        list all users.
        :return:
        """
        try:
            return self.client.user.listUsers(self.session)
        except xmlrpc.client.Fault as err:
            self.log.log_debug('api-call: user.listUsers')
            self.log.log_debug(f"Error: \n{err}")
            self.log.log.log_error('Unable to get list of users in SUSE Manager.')

    def user_getdetails(self, login_id):
        """
        Get the details of the given user.
        :param login_id:
        :return:
        """
        try:
            return self.client.user.getDetails(self.session, login_id)
        except xmlrpc.client.Fault as err:
            self.log.log_debug('api-call: user.getDetails')
            self.log.log_debug('Value passed: ')
            self.log.log_debug(f'  user_id:  {login_id}')
            self.log.log_debug(f"Error: \n{err}")
            self.log.log_error(f'Unable to get details of user with login {login_id}.')

    def user_listroles(self, login_id):
        """
        List the roles assigned to the user
        :param login_id:
        :return:
        """
        try:
            return self.client.user.listRoles(self.session, login_id)
        except xmlrpc.client.Fault as err:
            self.log.log_debug('api-call: user.listRoles')
            self.log.log_debug('Value passed: ')
            self.log.log_debug(f'  login_id:  {login_id}')
            self.log.log_debug(f"Error: \n{err}")
            self.log.log_error(f'Unable to get roles of user with login {login_id}.')

    def user_enable(self, login_id):
        """
        enable the given user
        :param login_id:
        :return:
        """
        try:
            return self.client.user.enable(self.session, login_id)
        except xmlrpc.client.Fault as err:
            self.log.log_debug('api-call: user.enable')
            self.log.log_debug('Value passed: ')
            self.log.log_debug(f'  login_id:  {login_id}')
            self.log.log_debug(f"Error: \n{err}")
            self.log.log_error(f'Unable to enable user with login {login_id}.')

    def user_create(self, login_id, password, first_name, last_name, mail, pam):
        """
        Create the given user
        :param login_id:
        :param password:
        :param first_name:
        :param last_name:
        :param mail:
        :param pam:
        :return:
        """
        try:
            return self.client.user.create(self.session, login_id, password, first_name, last_name, mail, pam)
        except xmlrpc.client.Fault as err:
            self.log.log_debug('api-call: user.create')
            self.log.log_debug('Value passed: ')
            self.log.log_debug(f'  login_id:  {login_id}')
            self.log.log_debug(f'  password:  {password}')
            self.log.log_debug(f'  first_name:  {first_name}')
            self.log.log_debug(f'  last_name:  {last_name}')
            self.log.log_debug(f'  email:  {mail}')
            self.log.log_debug(f'  usePamAuth:  {pam}')
            self.log.log_debug(f"Error: \n{err}")
            self.log.log_error(f'Unable to create user with login {login_id}.')

    def user_addrole(self, login_id, role):
        """
        Add the role to the user
        :param login_id:
        :param role:
        :return:
        """
        try:
            return self.client.user.addRole(self.session, login_id, role)
        except xmlrpc.client.Fault as err:
            self.log.log_debug('api-call: user.addRole')
            self.log.log_debug('Value passed: ')
            self.log.log_debug(f'  login_id:  {login_id}')
            self.log.log_debug(f'  password:  {role}')
            self.log.log_debug(f"Error: \n{err}")
            self.log.log_error(f'Unable to add role {role} to user with login {login_id}.')

    def user_removerole(self, login_id, role):
        """
        Remove the role from the user
        :param login_id:
        :param role:
        :return:
        """
        try:
            return self.client.user.removeRole(self.session, login_id, role)
        except xmlrpc.client.Fault as err:
            self.log.log_debug('api-call: user.removeRole')
            self.log.log_debug('Value passed: ')
            self.log.log_debug(f'  login_id:  {login_id}')
            self.log.log_debug(f'  password:  {role}')
            self.log.log_debug(f"Error: \n{err}")
            self.log.log_error(f'Unable to remove role {role} to user with login {login_id}.')

    def user_delete(self, login_id):
        """
        Delete the given user
        :param login_id:
        :return:
        """
        try:
            return self.client.user.delete(self.session, login_id)
        except xmlrpc.client.Fault as err:
            self.log.log_debug('api-call: user.delete')
            self.log.log_debug('Value passed: ')
            self.log.log_debug(f'  login_id:  {login_id}')
            self.log.log_debug(f"Error: \n{err}")
            self.log.log_error(f'Unable to delete user with login {login_id}.')

    def user_disable(self, login_id):
        """
        Disable the given user
        :param login_id:
        :return:
        """
        try:
            return self.client.user.disable(self.session, login_id)
        except xmlrpc.client.Fault as err:
            self.log.log_debug('api-call: user.disable')
            self.log.log_debug('Value passed: ')
            self.log.log_debug(f'  login_id:  {login_id}')
            self.log.log_debug(f"Error: \n{err}")
            self.log.log_error(f'Unable to disable user with login {login_id}.')

    def get_existing_users(self):
        """
        This will do:
        - login to sm
        - get existing users
        - check pam
        - get roles
        return:
        struct with users

        :return:
        """

        self.log.log_info("smtools: get_existing_users")
        existing_users = []
        self.suman_login()
        users = self.user_listusers()
        for record in users:
            details = self.user_getdetails(record["login"])
            if details["use_pam"]:
                existing_users.append({"id": record["id"], "login": record["login"], "enabled": details["enabled"],
                        "use_pam": details["use_pam"], "roles": self.user_listroles(record["login"])})
        return existing_users
