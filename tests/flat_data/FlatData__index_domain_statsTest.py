#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.data import FlatData;


def r_mock ( value ):
    if ( value == {} ):
        return None;
    return 'Mocked : {}'.format ( value );


class FlatData__index_domain_statsTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.data.extract_stat_value' ) as extract_stat_value:
            extract_stat_value.side_effect = r_mock;
            
            f = FlatData ();
            
            ret = f._index_domain_stats (
                domain_stats = [
                    { 'metric': 'random-metric-1', 'value': 'random-value-1' },
                    { 'metric': 'random-metric-2', 'value': 'random-value-2' },
                    { 'no-metric-key': 'another-value' }
                ]
            );
            
            self.assertEqual ( ret, {
                'random-metric-1': 'Mocked : random-value-1',
                'random-metric-2': 'Mocked : random-value-2'
            } );

            self.assertEqual ( extract_stat_value.call_count, 2 );
            extract_stat_value.assert_any_call (
                value = 'random-value-1'
            );
            extract_stat_value.assert_any_call (
                value = 'random-value-2'
            );


    def test_no_data ( self ):
        f = FlatData ();

        ret = f._index_domain_stats (
            domain_stats = []
        );

        self.assertEqual ( ret, {} );


if __name__ == '__main__':
    unittest.main ();
