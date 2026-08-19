#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.data import FlatData;


class FlatData__parse_delivery_errTest ( unittest.TestCase ):
    def test_calls ( self ):
        f = FlatData ();
        f.data [ 'random-key' ] = f._data_tpl.copy ();

        ret = f._parse_delivery_err (
            key = 'random-key',
            value = {
                'random-class-1__random-type-1': 0.12345,
                'random-class-1__random-type-2': 0.45678,
                'random-class-1__random-type-3': 0,
                'random-class-2__random-type-1': 0.7890,
                'random-class-2__random-type-2': None
            }
        );

        self.assertEqual ( ret, True );
        self.assertEqual ( f.data [ 'random-key' ] [ 'delivery_errors' ], [ {
            'class': 'random-class-1',
            'type': 'random-type-1',
            'percent': 12.35
        }, {
            'class': 'random-class-1',
            'type': 'random-type-2',
            'percent': 45.68
        }, {
            'class': 'random-class-2',
            'type': 'random-type-1',
            'percent': 78.9
        } ] );


    def test_no_value ( self ):
        f = FlatData ();
        f.data [ 'random-key' ] = f._data_tpl.copy ();

        ret = f._parse_delivery_err (
            key = 'random-key',
            value = {}
        );

        self.assertEqual ( ret, False );
        self.assertEqual ( f.data [ 'random-key' ] [ 'delivery_errors' ], [] );



if __name__ == '__main__':
    unittest.main ();
