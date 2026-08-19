#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.stats import Stats;


@patch ( 'googlepostmasterapi.base.Base.__init__', Mock ( return_value = None ) )
class Stats_add_err_httpTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.stats.Stats.add_err' ) as add_err:
            s = Stats ();
            s.data = { 'err_http': {} };
            
            s.add_err_http (
                code = 123,
                err = 'random-err',
                domain = 'random-domain'
            );
            
            add_err.assert_called_once_with ();
            self.assertEqual ( 123 in s.data [ 'err_http' ], True );
            self.assertTrue ( s.data [ 'err_http' ] [ 123 ] [ 'count' ], 1 );
            self.assertTrue ( s.data [ 'err_http' ] [ 123 ] [ 'domains' ], [ 'random-domain' ] );
            self.assertTrue ( s.data [ 'err_http' ] [ 123 ] [ 'message' ], 'random-err' );

            
    def test_new_err ( self ):
        with patch ( 'googlepostmasterapi.stats.Stats.add_err' ) as add_err:
            s = Stats ();
            s.data = { 'err_http': {
                'another-code': { 'count': 12, 'domains': [ 'another-domain-1', 'another-domain-2' ], 'message': 'another-message' }
            } };
            
            s.add_err_http (
                code = 123,
                err = 'random-err',
                domain = 'random-domain'
            );
            
            add_err.assert_called_once_with ();
            self.assertEqual ( s.data [ 'err_http' ], {
                'another-code': { 'count': 12, 'domains': [ 'another-domain-1', 'another-domain-2' ], 'message': 'another-message' },
                123: { 'count': 1, 'domains': [ 'random-domain' ], 'message': 'random-err' }
            } );

            
    def test_add_domain ( self ):
        with patch ( 'googlepostmasterapi.stats.Stats.add_err' ) as add_err:
            s = Stats ();
            s.data = { 'err_http': {
                123: { 'count': 12, 'domains': [ 'random-domain-1', 'random-domain-2' ], 'message': 'random-message' }
            } };
            
            s.add_err_http (
                code = 123,
                err = 'another-message',
                domain = 'random-domain-3'
            );
            
            add_err.assert_called_once_with ();
            self.assertEqual ( s.data [ 'err_http' ] [ 123 ] [ 'count' ], 13 );
            self.assertEqual ( s.data [ 'err_http' ] [ 123 ] [ 'domains' ], [ 'random-domain-1', 'random-domain-2', 'random-domain-3' ] );
            self.assertEqual ( s.data [ 'err_http' ] [ 123 ] [ 'message' ], 'random-message' );
            
            
if __name__ == '__main__':
    unittest.main ();
