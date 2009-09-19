#!/usr/bin/env python
""" Management script to check for compliance with
version control workflow & catch files being updated
on the production webserver"""

import ConfigParser
import logging
import os
import unittest
import argparse

class GitComply:
    "Checks for files etc"

    def __init__(self):
        config = ConfigParser.RawConfigParser()
        if args.configfile:
            config_location = args.configfile
        else:
            config_location = os.getenv('HOME')
        configfile = os.path.join(config_location,'.gitcomply')
        config.read(configfile)
        self.config = {'email': config.get('admin', 'email')}


if __name__ == '__main__':
    package_description = """Check for uncommitted files in git repos"""
    parser = argparse.ArgumentParser(description=package_description)
    parser.add_argument('-c', '--configfile',
                        help="override default .gitcomply location")
    args = parser.parse_args()

    # Initialize class
    gitcomply = GitComply()

    print gitcomply.config['email']
