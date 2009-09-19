#!/usr/bin/env python
""" Management script to check for compliance with
version control workflow & catch files being updated
on the production webserver"""

import ConfigParser
import logging
import os
import re
import subprocess
import argparse

# Define logging behaviour
config_logger = logging.getLogger( 'config' )
search_logger = logging.getLogger( 'search' )
status_logger = logging.getLogger( 'status' )
logformat = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
formatter = logging.Formatter( logformat )
config_logger.setLevel( logging.DEBUG )
search_logger.setLevel( logging.DEBUG )
status_logger.setLevel( logging.DEBUG )
fh = logging.FileHandler( '.gitcomply.log' )
fh.setLevel( logging.ERROR )
fh.setFormatter( formatter )
ch = logging.StreamHandler()
ch.setLevel( logging.DEBUG )
ch.setFormatter( formatter )
config_logger.addHandler( ch)
search_logger.addHandler( ch )
status_logger.addHandler( fh )
status_logger.addHandler( ch )

class GitComply:
    "Checks for files etc"

    def search( self ):
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


    def status( self ):
        for repo in self.repos:
            os.chdir( repo )
            status_cmd = [ 'git', 'status' ]
            status = subprocess.Popen( status_cmd, stdout=subprocess.PIPE ).communicate()[0]
            modfiles = self.mod_re.findall( status )
            if len( modfiles ) > 0:
                for filename in modfiles:
                    self.warnings.append( WarningFile( filename, repo, 'modified' ) )
            newfiles = self.new_re.findall ( status )
            if len( newfiles ) > 0:
                splitfiles_re = re.compile( r'([\.\w]+)' )
                new_file_list = splitfiles_re.findall( newfiles[0] )
                for filename in new_file_list:
                    self.warnings.append( WarningFile( filename, repo, 'added') )
        return self.warnings


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
        self.warnings = []
        if self.args.directory:
            self.dir = args.directory
        else:
            self.dir = os.getcwd()
        search_logger.debug( "Directory: %s" % self.dir )
        self.mod_re = re.compile( r'modified:(.*)' )
        self.new_re = re.compile( r'Untracked files:.*\n#(\n#\t.*)no changes',
                                  re.DOTALL )

class WarningFile:
    """Holds individual warnings"""

    def __init__( self, filename=None, repo=None, warning_type=None ):
        self.filename = filename
        self.repo = repo
        self.type = warning_type

                
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

    config_logger.debug( "email: %s" % gitcomply.config['email'] )

    # Search for repos
    gitcomply.search()

    for repo in gitcomply.repos:
        search_logger.debug( "repo: %s" % repo )

    # Check status
    gitcomply.status()
    
    for warning in gitcomply.warnings:
        status_logger.debug( "warning: %s " % warning.filename )
