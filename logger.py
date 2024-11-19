#!/usr/bin/env python3
#
# Script: logger.py
#
# Description: This script contains standard function for logging#

# coding: utf-8

"""
This library contains functions used in other modules
"""

import constants
import os
import sys
import logging


class Logging:
    error_text = ""
    error_found = False
    def __init__(self):
        log_dir = constants.CONFIGSM['log_dir']
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_name = os.path.join(log_dir, "sm-ldap-users.log")
        formatter = logging.Formatter('%(asctime)s |  %(levelname)s | %(message)s',
                                      '%d-%m-%Y %H:%M:%S')
        fh = logging.FileHandler(log_name, 'a')
        fh.setLevel(constants.CONFIGSM['log_level'].upper())
        fh.setFormatter(formatter)
        console = logging.StreamHandler()
        console.setLevel(constants.CONFIGSM['log_level'].upper())
        console.setFormatter(formatter)
        self.log = logging.getLogger('')
        self.log.setLevel(logging.DEBUG)
        self.log.addHandler(console)
        self.log.addHandler(fh)

    def minor_error(self, errtxt):
        """
        Print minor error.
        """
        self.error_text += errtxt
        self.error_text += "\n"
        self.error_found = True
        self.log_error(errtxt)

    def fatal_error(self, errtxt):
        """
        log fatal error and exit program
        """
        self.error_text += errtxt
        self.error_text += "\n"
        self.error_found = True
        self.log_error("{}".format(errtxt))
        sys.exit(1)

    def log_info(self, errtxt):
        """
        Log info text
        """
        self.log.info("{}".format(errtxt))

    def log_error(self, errtxt):
        """
        Log error text
        """
        self.log.error("{}".format(errtxt))

    def log_warning(self, errtxt):
        """
        Log error text
        """
        self.log.warning("{}".format(errtxt))

    def log_debug(self, errtxt):
        """
        Log debug text
        :param errtxt :
        :return:
        """
        self.log.debug("{}".format(errtxt))
