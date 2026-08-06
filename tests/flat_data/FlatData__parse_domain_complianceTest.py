#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.data import FlatData;


def r_mock ( status ):
    if ( status is None ):
        return None;
    return 'Mocked : {}'.format ( status );


class FlatData__parse_domain_complianceTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.data.FlatData._parse_status' ) as parse_status:
            parse_status.side_effect = r_mock;
            
            f = FlatData ();
            f.data [ 'random-key' ] = f._data_tpl.copy ();

            ret = f._parse_domain_compliance (
                key = 'random-key',
                value = {
                    'domainId': 'random-domain',
                    'deliverabilityStatusVerdict': {
                        'state': 'random-dsv-state',
                        'reason': 'random-dsv-reason',
                    },
                    'oneClickUnsubscribeVerdict': {
                        'status': 'random-ocuv-status',
                        'reason': 'random-ocuv-reason'
                    },
                    'honorUnsubscribeVerdict': {
                        'status': 'random-huv-status',
                        'reason': 'random-huv-reason',
                    },
                    'rowData': [ {
                        'requirement': 'random-rd-1-requirement',
                        'status': 'random-rd-1-status'
                    }, {
                        'requirement': 'random-rd-2-requirement',
                        'status': 'random-rd-2-status'
                    } ]
                }
            );

            self.assertEqual ( ret, True );
            self.assertEqual ( f.data [ 'random-key' ] [ 'domain_compliance' ], {
                'deliverability': {
                    'status': 'Mocked : random-dsv-state',
                    'reason': 'random-dsv-reason'
                },
                'one_click_unsubscribe': {
                    'status': 'Mocked : random-ocuv-status',
                    'reason': 'random-ocuv-reason'
                },
                'honor_unsubscribe': {
                    'status': 'Mocked : random-huv-status',
                    'reason': 'random-huv-reason'
                },
                'checks': [ {
                    'check': 'random-rd-1-requirement',
                    'status': 'Mocked : random-rd-1-status'
                }, {
                    'check': 'random-rd-2-requirement',
                    'status': 'Mocked : random-rd-2-status'
                } ]
            } );

            self.assertEqual ( parse_status.call_count, 5 );
            parse_status.assert_any_call ( status = 'random-dsv-state' );
            parse_status.assert_any_call ( status = 'random-ocuv-status' );
            parse_status.assert_any_call ( status = 'random-huv-status' );
            parse_status.assert_any_call ( status = 'random-rd-1-status' );
            parse_status.assert_any_call ( status = 'random-rd-2-status' );

            
    def test_value_empty_dict ( self ):
        with patch ( 'googlepostmasterapi.data.FlatData._parse_status' ) as parse_status:
            parse_status.side_effect = r_mock;
            
            f = FlatData ();
            f.data [ 'random-key' ] = f._data_tpl.copy ();

            ret = f._parse_domain_compliance (
                key = 'random-key',
                value = {}
            );

            self.assertEqual ( ret, True );
            self.assertEqual ( f.data [ 'random-key' ] [ 'domain_compliance' ], {
                'deliverability': {
                    'status': None,
                    'reason': None
                },
                'one_click_unsubscribe': {
                    'status': None,
                    'reason': None
                },
                'honor_unsubscribe': {
                    'status': None,
                    'reason': None
                },
                'checks': []
            } );

            self.assertEqual ( parse_status.call_count, 3 );
            parse_status.assert_any_call ( status = None );


    def test_no_value ( self ):
        f = FlatData ();
        f.data [ 'random-key' ] = f._data_tpl.copy ();
    
        ret = f._parse_domain_compliance (
            key = 'random-key',
            value = None
        );
    
        self.assertEqual ( ret, False );
        self.assertEqual ( f.data [ 'random-key' ] [ 'domain_compliance' ], None );


if __name__ == '__main__':
    unittest.main ();
