#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.data import FlatData;


@patch ( 'googlepostmasterapi.base.Base.__init__', Mock ( return_value = None ) )
class FlatData__parse_crypted_inboundTest ( unittest.TestCase ):
    def test_calls ( self ):
        f = FlatData ();
        f.data [ 'random-key' ] = f._data_tpl.copy ();
        
        ret = f._parse_crypted_inbound (
            key = 'random-key',
            value = '0.45678'
        );
        
        self.assertEqual ( ret, True );
        self.assertEqual ( f.data [ 'random-key' ] [ 'tls_inbound_percent' ], 45.68 );

        
    def test_no_value ( self ):
        f = FlatData ();
        f.data [ 'random-key' ] = f._data_tpl.copy ();
        
        ret = f._parse_crypted_inbound (
            key = 'random-key',
            value = None
        );
        
        self.assertEqual ( ret, False );
        self.assertEqual ( f.data [ 'random-key' ] [ 'tls_inbound_percent' ], None );
        
        
if __name__ == '__main__':
    unittest.main ();
