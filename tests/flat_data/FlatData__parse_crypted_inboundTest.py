#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.data import FlatData;


class FlatData__parse_crypted_inboundTest ( unittest.TestCase ):
    def test_calls ( self ):
        p = FlatData ();
        p.data [ 'random-key' ] = p._data_tpl.copy ();
        
        ret = p._parse_crypted_inbound (
            key = 'random-key',
            value = '0.4567'
        );
        
        self.assertEqual ( ret, True );
        self.assertEqual ( p.data [ 'random-key' ] [ 'tls_inbound_percent' ], 45.7 );

        
    def test_no_value ( self ):
        p = FlatData ();
        p.data [ 'random-key' ] = p._data_tpl.copy ();
        
        ret = p._parse_crypted_inbound (
            key = 'random-key',
            value = None
        );
        
        self.assertEqual ( ret, False );
        self.assertEqual ( p.data [ 'random-key' ] [ 'tls_inbound_percent' ], None );
        
        
if __name__ == '__main__':
    unittest.main ();
