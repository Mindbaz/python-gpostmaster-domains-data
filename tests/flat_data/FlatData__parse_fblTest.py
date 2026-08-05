#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.data import FlatData;


class FlatData__parse_fblTest ( unittest.TestCase ):
    def test_calls ( self ):
        f = FlatData ();
        f.data [ 'random-key' ] = f._data_tpl.copy ();

        ret = f._parse_fbl (
            key = 'random-key',
            value = {
                '123': 0.1234,
                '456': 0.4567
            }
        );

        self.assertEqual ( ret, True );
        self.assertEqual ( f.data [ 'random-key' ] [ 'feedback_loop' ] [ 'nb_row' ], 2 );
        self.assertEqual ( f.data [ 'random-key' ] [ 'feedback_loop' ] [ 'percent_per_uid' ], [ {
            'uid': 123,
            'spam_percent': 12.3
        }, {
            'uid': 456, 'spam_percent': 45.7
        } ] );


    def test_no_value ( self ):
        f = FlatData ();
        f.data [ 'random-key' ] = f._data_tpl.copy ();

        ret = f._parse_fbl (
            key = 'random-key',
            value = {}
        );

        self.assertEqual ( ret, False );
        self.assertEqual ( f.data [ 'random-key' ] [ 'feedback_loop' ] [ 'nb_row' ], 0 );
        self.assertEqual ( f.data [ 'random-key' ] [ 'feedback_loop' ] [ 'percent_per_uid' ], [] );


    def test_missing_value_for_id ( self ):
        f = FlatData ();
        f.data [ 'random-key' ] = f._data_tpl.copy ();

        ret = f._parse_fbl (
            key = 'random-key',
            value = {
                '123': None,
                '456': 0.4567
            }
        );

        self.assertEqual ( ret, True );
        self.assertEqual ( f.data [ 'random-key' ] [ 'feedback_loop' ] [ 'nb_row' ], 1 );
        self.assertEqual ( f.data [ 'random-key' ] [ 'feedback_loop' ] [ 'percent_per_uid' ], [ {
            'uid': 456,
            'spam_percent': 45.7
        } ] );


    def test_non_numeric_id ( self ):
        f = FlatData ();
        f.data [ 'random-key' ] = f._data_tpl.copy ();

        ret = f._parse_fbl (
            key = 'random-key',
            value = {
                'random-non-numeric-id': 0.1234
            }
        );

        self.assertEqual ( ret, True );
        self.assertEqual ( f.data [ 'random-key' ] [ 'feedback_loop' ] [ 'nb_row' ], 1 );
        self.assertEqual ( f.data [ 'random-key' ] [ 'feedback_loop' ] [ 'percent_per_uid' ], [ {
            'uid': 'random-non-numeric-id',
            'spam_percent': 12.3
        } ] );


if __name__ == '__main__':
    unittest.main ();
