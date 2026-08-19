#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from datetime import datetime;


from googlepostmasterapi.logger import LoggingFilter;
import logging;


class RMock ( logging.LogRecord ):
    def __init__ ( self, *args, **kargs ):
        print ( 'RMock : __init__' );
        self.levelno = args [ 0 ];
        pass;
    

class PubBase_filterTest ( unittest.TestCase ):
    def test_calls ( self ):
        l = LoggingFilter (
            level = 123
        );
        
        self.assertEqual ( l.filter ( RMock ( 122 ) ), True );
        self.assertEqual ( l.filter ( RMock ( 123 ) ), False );
        self.assertEqual ( l.filter ( RMock ( 124 ) ), False );
            
        
if __name__ == '__main__':
    unittest.main ();
