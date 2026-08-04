#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.stats import Stats;


class Stats_constructorTest ( unittest.TestCase ):
    def test_constructor ( self ):
        s = Stats ();
        
        self.assertEqual ( type ( s.data ), dict );
        self.assertEqual ( s.data [ 'total' ], 0 );
        self.assertEqual ( s.data [ 'ok' ], 0 );
        self.assertEqual ( s.data [ 'err' ], 0 );
        self.assertEqual ( s.data [ 'err_http' ], {} );

                        
            
if __name__ == '__main__':
    unittest.main ();
