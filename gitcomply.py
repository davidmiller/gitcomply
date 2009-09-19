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

    def search(self):
        """Searches for git repos"""
        if self.args.recursive:
            for root, dirs, files in os.walk( self.dir ):
                for dir in dirs:
                    if dir == '.git':
                        self.repos.append( root )
            return self.repos
        
        else:
            if os.path.exists( '.git' ):
                self.repos.append( self.dir )
            return self.repos


    def __init__( self, args ):
        config = ConfigParser.RawConfigParser()
        if args.configfile:
            config_location = args.configfile
        else:
            config_location = os.getenv( 'HOME' )
        configfile = os.path.join( config_location,'.gitcomply' )
        config.read(configfile)
        self.config = { 'email': config.get( 'admin', 'email' ) }
        self.args = args
        self.repos = []
        if self.args.directory:
            self.dir = os.getcwd()
        else:
            self.dir = os.getcwd()


if __name__ == '__main__':
    package_description = """Check for uncommitted files in git repos"""
    parser = argparse.ArgumentParser( description=package_description )
    parser.add_argument( '-c', '--configfile',
                        help="override default .gitcomply location" )
    parser.add_argument( '-d', '--directory',
                         help="directory in which to begin search" )
    parser.add_argument( '-r', '--recursive',
                         action='store_true',
                         help="check in all repos recursively" )
    args = parser.parse_args()

    # Initialize class
    gitcomply = GitComply( args )

    # Search for repos
    gitcomply.search()
    
    print gitcomply.config['email']
    for repo in gitcomply.repos:
        print repo
