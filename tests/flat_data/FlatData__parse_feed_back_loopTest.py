#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.data import FlatData;


class FlatData__parse_feed_back_loopTest ( unittest.TestCase ):
    def test_calls ( self ):
        p = FlatData ();
        p.data [ 'random-key' ] = p._data_tpl.copy ();
        
        ret = p._parse_feed_back_loop (
            key = 'random-key',
            value = [
                { 'id': '123', 'spamRatio': 0.1234 },
                { 'id': '456', 'spamRatio': 0.4567 },
            ]
        );
            
        self.assertEqual ( ret, True );
        self.assertEqual ( p.data [ 'random-key' ] [ 'feedback_loop' ] [ 'nb_row' ], 2 );
        self.assertEqual ( p.data [ 'random-key' ] [ 'feedback_loop' ] [ 'percent_per_uid' ], [
            { 'uid': 123, 'spam_percent': 12.3 },
            { 'uid': 456, 'spam_percent': 45.7 }
        ] );

        
    def test_no_value ( self ):
        p = FlatData ();
        p.data [ 'random-key' ] = p._data_tpl.copy ();
        
        ret = p._parse_feed_back_loop (
            key = 'random-key',
            value = None
        );
        
        self.assertEqual ( ret, False );
        self.assertEqual ( p.data [ 'random-key' ] [ 'feedback_loop' ] [ 'nb_row' ], 0 );
        self.assertEqual ( p.data [ 'random-key' ] [ 'feedback_loop' ] [ 'percent_per_uid' ], [] );

        
    def test_missing_field_spamRatio ( self ):
        p = FlatData ();
        p.data [ 'random-key' ] = p._data_tpl.copy ();
        
        ret = p._parse_feed_back_loop (
            key = 'random-key',
            value = [
                { 'id': '123' },
                { 'id': '456', 'spamRatio': 0.4567 },
            ]
        );
            
        self.assertEqual ( ret, True );
        self.assertEqual ( p.data [ 'random-key' ] [ 'feedback_loop' ] [ 'nb_row' ], 1 );
        self.assertEqual ( p.data [ 'random-key' ] [ 'feedback_loop' ] [ 'percent_per_uid' ], [
            { 'uid': 456, 'spam_percent': 45.7 }
        ] );


if __name__ == '__main__':
    unittest.main ();
