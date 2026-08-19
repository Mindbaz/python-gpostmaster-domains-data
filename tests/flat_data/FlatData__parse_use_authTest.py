#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.data import FlatData;


@patch ( 'googlepostmasterapi.base.Base.__init__', Mock ( return_value = None ) )
class FlatData__parse_use_authTest ( unittest.TestCase ):
    def test_calls ( self ):
        f = FlatData ();
        f.data [ 'random-key' ] = f._data_tpl.copy ();
        
        ret = f._parse_use_auth (
            key = 'random-key',
            dkim = '0.12345',
            spf = '0.45678',
            dmarc = '0.7890'
        );
            
        self.assertEqual ( ret, True );
        self.assertEqual ( f.data [ 'random-key' ] [ 'auth_use_dkim_percent' ], 12.35 );
        self.assertEqual ( f.data [ 'random-key' ] [ 'auth_use_spf_percent' ], 45.68 );
        self.assertEqual ( f.data [ 'random-key' ] [ 'auth_use_dmarc_percent' ], 78.9 );

        
    def test_no_dkim ( self ):
        f = FlatData ();
        f.data [ 'random-key' ] = f._data_tpl.copy ();
        
        ret = f._parse_use_auth (
            key = 'random-key',
            spf = '0.45678',
            dmarc = '0.7890'
        );
            
        self.assertEqual ( ret, True );
        self.assertEqual ( f.data [ 'random-key' ] [ 'auth_use_dkim_percent' ], None );
        self.assertEqual ( f.data [ 'random-key' ] [ 'auth_use_spf_percent' ], 45.68 );
        self.assertEqual ( f.data [ 'random-key' ] [ 'auth_use_dmarc_percent' ], 78.9 );

        
    def test_no_spf ( self ):
        f = FlatData ();
        f.data [ 'random-key' ] = f._data_tpl.copy ();
        
        ret = f._parse_use_auth (
            key = 'random-key',
            dkim = '0.12345',
            dmarc = '0.7890'
        );
            
        self.assertEqual ( ret, True );
        self.assertEqual ( f.data [ 'random-key' ] [ 'auth_use_dkim_percent' ], 12.35 );
        self.assertEqual ( f.data [ 'random-key' ] [ 'auth_use_spf_percent' ], None );
        self.assertEqual ( f.data [ 'random-key' ] [ 'auth_use_dmarc_percent' ], 78.9 );

        
    def test_no_dmarc ( self ):
        f = FlatData ();
        f.data [ 'random-key' ] = f._data_tpl.copy ();
        
        ret = f._parse_use_auth (
            key = 'random-key',
            dkim = '0.12345',
            spf = '0.45678'
        );
            
        self.assertEqual ( ret, True );
        self.assertEqual ( f.data [ 'random-key' ] [ 'auth_use_dkim_percent' ], 12.35 );
        self.assertEqual ( f.data [ 'random-key' ] [ 'auth_use_spf_percent' ], 45.68 );
        self.assertEqual ( f.data [ 'random-key' ] [ 'auth_use_dmarc_percent' ], None );

        
    def test_no_one ( self ):
        f = FlatData ();
        
        ret = f._parse_use_auth (
            key = 'random-key',);
        f.data [ 'random-key' ] = f._data_tpl.copy ();
            
        self.assertEqual ( ret, False );
        self.assertEqual ( f.data [ 'random-key' ] [ 'auth_use_dkim_percent' ], None );
        self.assertEqual ( f.data [ 'random-key' ] [ 'auth_use_spf_percent' ], None );
        self.assertEqual ( f.data [ 'random-key' ] [ 'auth_use_dmarc_percent' ], None );

        
    def test_values_none ( self ):
        f = FlatData ();
        f.data [ 'random-key' ] = f._data_tpl.copy ();
        
        ret = f._parse_use_auth (
            key = 'random-key',
            dkim = None,
            spf = None,
            dmarc = None
        );
        
        self.assertEqual ( ret, False );
        self.assertEqual ( f.data [ 'random-key' ] [ 'auth_use_dkim_percent' ], None );
        self.assertEqual ( f.data [ 'random-key' ] [ 'auth_use_spf_percent' ], None );
        self.assertEqual ( f.data [ 'random-key' ] [ 'auth_use_dmarc_percent' ], None );


if __name__ == '__main__':
    unittest.main ();
