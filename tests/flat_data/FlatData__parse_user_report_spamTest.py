#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.data import FlatData;


class FlatData__parse_user_report_spamTest ( unittest.TestCase ):
    def test_calls ( self ):
        f = FlatData ();
        f.data [ 'random-key' ] = f._data_tpl.copy ();
        
        ret = f._parse_user_report_spam ( key = 'random-key', value = '0.1234' );
        self.assertEqual ( ret, True );
        self.assertEqual ( f.data [ 'random-key' ] [ 'user_report_spam_percent' ], 12.3 );

        
    def test_no_value ( self ):
        f = FlatData ();
        f.data [ 'random-key' ] = f._data_tpl.copy ();
        
        ret = f._parse_user_report_spam ( key = 'random-key', value = None );
        self.assertEqual ( ret, False );
        self.assertEqual ( f.data [ 'random-key' ] [ 'user_report_spam_percent' ], None );

        
if __name__ == '__main__':
    unittest.main ();
