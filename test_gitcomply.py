#!/usr/bin/env python
import unittest
import argparse
from gitcomply import GitComply

class MyTest( unittest.TestCase ):


    def testTrue( self ):
        args = argparse.Namespace( configfile=None,
                                   directory=None,
                                   email=False,
                                   recursive=False )
        gitcomply = GitComply( args )
        try:
            result = gitcomply.search()
            expected = [ '/home/david/python/gitcomply' ]
            self.assertTrue( result == expected )
        finally:
            pass

    def testFalse( self ):
        args = argparse.Namespace( configfile=None,
                                   directory=None,
                                   email=False,
                                   recursive=False )
        gitcomply = GitComply( args )
        try:
            result = gitcomply.search()
            expected = [ '' ]
            self.assertFalse( result == expected )
        finally:
            pass


if __name__ == '__main__':
    unittest.main()
