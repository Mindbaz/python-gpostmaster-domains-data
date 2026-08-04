#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.stats import Stats;


class Stats__print_statsTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.stats.write_std' ) as write_std:
            s = Stats ();
            s.data = {
                'total': 202,
                'ok': 20,
                'err': 50,
                'err_http': {
                    123: { 'count': 48, 'domains': [ 'random-domain-123-1', 'random-domain-123-2' ] },
                    456: { 'count': 23, 'domains': [ 'random-domain-456-1' ] }
                }
            };
            
            ret = s.print_stats ();
            self.assertEqual ( ret, True );
            self.assertEqual ( write_std.call_count, 3 );
            
            for call in write_std.call_args_list:
                args, kwargs = call;
                pprint ( args );
                pprint ( kwargs );
                
            write_std.assert_any_call ( [
                'Total calls : 202',
                'Total calls success : 20 (9.9%)',
                'Total calls error : 50 (24.8%)'
            ] );
                
            write_std.assert_any_call ( [
                'Total calls error http 123 : 48 (23.8%)',
                'Domains : random-domain-123-1 / random-domain-123-2'
            ] );
            
            write_std.assert_any_call ( [
                'Total calls error http 456 : 23 (11.4%)',
                'Domains : random-domain-456-1'
            ] );
    
                
    def test_no_http_error ( self ):
        with patch ( 'googlepostmasterapi.stats.write_std' ) as write_std:
            s = Stats ();
            s.data = {
                'total': 202,
                'ok': 20,
                'err': 50,
                'err_http': {}
            };
            
            ret = s.print_stats ();
            self.assertEqual ( ret, True );
            write_std.assert_called_once_with ( [
                'Total calls : 202',
                'Total calls success : 20 (9.9%)',
                'Total calls error : 50 (24.8%)'
            ] );
    
                
    def test_nothing_to_print ( self ):
        with patch ( 'googlepostmasterapi.stats.write_std' ) as write_std:
            s = Stats ();
            s.data = {
                'total': 0
            };
            
            ret = s.print_stats ();
            self.assertEqual ( ret, False );
            write_std.assert_not_called ();

            
if __name__ == '__main__':
    unittest.main ();
