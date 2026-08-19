#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.stats import Stats;


class Stats_constructorTest ( unittest.TestCase ):
    def test_constructor ( self ):
        with patch ( 'googlepostmasterapi.base.Base.__init__' ) as super_:
            s = Stats ();
            
            self.assertEqual ( type ( s.data ), dict );
            self.assertEqual ( s.data [ 'total' ], 0 );
            self.assertEqual ( s.data [ 'ok' ], 0 );
            self.assertEqual ( s.data [ 'err' ], 0 );
            self.assertEqual ( s.data [ 'err_http' ], {} );

            super_.asser_called_once_with (
                verbose = True
            );


    def test_inheritance ( self ):
        check = False;
        for inherit in Stats.__mro__:
            if ( inherit.__name__ == 'Base' ):
                check = True;
                break;
        self.assertEqual ( check, True );

                        
            
if __name__ == '__main__':
    unittest.main ();
