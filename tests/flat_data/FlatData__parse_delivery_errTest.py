#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;

from googlepostmasterapi.data import FlatData;

class FlatData__parse_delivery_errTest ( unittest.TestCase ):
    def test_calls ( self ):
        p = FlatData ();
        p.data [ 'random-key' ] = p._data_tpl.copy ();
                
        ret = p._parse_delivery_err (
            key = 'random-key',
            value = [
                { 'errorClass': 'RANDOM-CLASS-1', 'errorType': 'RANDOM-TYPE-1', 'errorRatio': 0.1234 },
                { 'errorClass': 'RANDOM-CLASS-1', 'errorType': 'RANDOM-TYPE-2', 'errorRatio': 0.4567 },
                { 'errorClass': 'RANDOM-CLASS-2', 'errorType': 'RANDOM-TYPE-1', 'errorRatio': 0.789 },
                { 'errorClass': 'RANDOM-CLASS-2', 'errorType': 'RANDOM-TYPE-2' }
            ]
        );
        
        self.assertEqual ( ret, True );
        self.assertEqual ( p.data [ 'random-key' ] [ 'delivery_errors' ], [
            { 'type': 'random-type-1', 'class': 'random-class-1', 'percent': 12.3 },
            { 'type': 'random-type-2', 'class': 'random-class-1', 'percent': 45.7 },
            { 'type': 'random-type-1', 'class': 'random-class-2', 'percent': 78.9 }
        ] );

        
    def test_no_value ( self ):
        p = FlatData ();
        p.data [ 'random-key' ] = p._data_tpl.copy ();
        
        ret = p._parse_delivery_err (
            key = 'random-key',
            value = None
        );
        
        self.assertEqual ( ret, False );
        self.assertEqual ( p.data [ 'random-key' ] [ 'delivery_errors' ], [] );

        
        
if __name__ == '__main__':
    unittest.main ();
