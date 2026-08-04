#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.data import FlatData;


class FlatData__parse_use_authTest ( unittest.TestCase ):
    def test_calls ( self ):
        p = FlatData ();
        p.data [ 'random-key' ] = p._data_tpl.copy ();
        
        ret = p._parse_use_auth (
            key = 'random-key',
            dkim = '0.1234',
            spf = '0.4567',
            dmarc = '0.789'
        );
            
        self.assertEqual ( ret, True );
        self.assertEqual ( p.data [ 'random-key' ] [ 'auth_use_dkim_percent' ], 12.3 );
        self.assertEqual ( p.data [ 'random-key' ] [ 'auth_use_spf_percent' ], 45.7 );
        self.assertEqual ( p.data [ 'random-key' ] [ 'auth_use_dmarc_percent' ], 78.9 );

        
    def test_no_dkim ( self ):
        p = FlatData ();
        p.data [ 'random-key' ] = p._data_tpl.copy ();
        
        ret = p._parse_use_auth (
            key = 'random-key',
            spf = '0.4567',
            dmarc = '0.789'
        );
            
        self.assertEqual ( ret, True );
        self.assertEqual ( p.data [ 'random-key' ] [ 'auth_use_dkim_percent' ], None );
        self.assertEqual ( p.data [ 'random-key' ] [ 'auth_use_spf_percent' ], 45.7 );
        self.assertEqual ( p.data [ 'random-key' ] [ 'auth_use_dmarc_percent' ], 78.9 );

        
    def test_no_spf ( self ):
        p = FlatData ();
        p.data [ 'random-key' ] = p._data_tpl.copy ();
        
        ret = p._parse_use_auth (
            key = 'random-key',
            dkim = '0.1234',
            dmarc = '0.789'
        );
            
        self.assertEqual ( ret, True );
        self.assertEqual ( p.data [ 'random-key' ] [ 'auth_use_dkim_percent' ], 12.3 );
        self.assertEqual ( p.data [ 'random-key' ] [ 'auth_use_spf_percent' ], None );
        self.assertEqual ( p.data [ 'random-key' ] [ 'auth_use_dmarc_percent' ], 78.9 );

        
    def test_no_dmarc ( self ):
        p = FlatData ();
        p.data [ 'random-key' ] = p._data_tpl.copy ();
        
        ret = p._parse_use_auth (
            key = 'random-key',
            dkim = '0.1234',
            spf = '0.4567'
        );
            
        self.assertEqual ( ret, True );
        self.assertEqual ( p.data [ 'random-key' ] [ 'auth_use_dkim_percent' ], 12.3 );
        self.assertEqual ( p.data [ 'random-key' ] [ 'auth_use_spf_percent' ], 45.7 );
        self.assertEqual ( p.data [ 'random-key' ] [ 'auth_use_dmarc_percent' ], None );

        
    def test_no_one ( self ):
        p = FlatData ();
        
        ret = p._parse_use_auth (
            key = 'random-key',);
        p.data [ 'random-key' ] = p._data_tpl.copy ();
            
        self.assertEqual ( ret, False );
        self.assertEqual ( p.data [ 'random-key' ] [ 'auth_use_dkim_percent' ], None );
        self.assertEqual ( p.data [ 'random-key' ] [ 'auth_use_spf_percent' ], None );
        self.assertEqual ( p.data [ 'random-key' ] [ 'auth_use_dmarc_percent' ], None );

        
    def test_values_none ( self ):
        p = FlatData ();
        p.data [ 'random-key' ] = p._data_tpl.copy ();
        
        ret = p._parse_use_auth (
            key = 'random-key',
            dkim = None,
            spf = None,
            dmarc = None
        );
        
        self.assertEqual ( ret, False );
        self.assertEqual ( p.data [ 'random-key' ] [ 'auth_use_dkim_percent' ], None );
        self.assertEqual ( p.data [ 'random-key' ] [ 'auth_use_spf_percent' ], None );
        self.assertEqual ( p.data [ 'random-key' ] [ 'auth_use_dmarc_percent' ], None );


if __name__ == '__main__':
    unittest.main ();
