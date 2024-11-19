#!/usr/bin/env python3
#
# Script: logger.py
#
# Description: This script contains standard function for logging#

# coding: utf-8

"""
This library contains functions used in other modules
"""

import yaml
import os
import sys

def load_yaml(stream):
    """
    Load YAML data.
    """
    loader = yaml.Loader(stream)
    try:
        return loader.get_single_data()
    finally:
        loader.dispose()

if not os.path.isfile(os.path.dirname(__file__) + "/configsm.yaml"):
    print("ERROR: configsm.yaml doesn't exist. Please create file")
    sys.exit(1)
else:
    with open(os.path.dirname(__file__) + '/configsm.yaml') as h_cfg:
        CONFIGSM = load_yaml(h_cfg)

SM_ROLES = ["activation_key_admin", "channel_admin", "config_admin", "image_admin", "org_admin", "satellite_admin", "system_group_admin"]
USER_ATTRIBUTES = ['sAMAccountName','givenName', 'sn', 'mail']