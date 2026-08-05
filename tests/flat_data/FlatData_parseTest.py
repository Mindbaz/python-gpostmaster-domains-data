#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.data import FlatData;


class FlatData_parseTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.data.copy.deepcopy' ) as deepcopy:
            with patch ( 'googlepostmasterapi.data.FlatData._index_domain_stats' ) as index_domain_stats:
                with patch ( 'googlepostmasterapi.data.FlatData._parse_user_report_spam' ) as parse_user_report_spam:
                    with patch ( 'googlepostmasterapi.data.FlatData._parse_domain_compliance' ) as parse_domain_compliance:
                        with patch ( 'googlepostmasterapi.data.FlatData._parse_fbl' ) as parse_fbl:
                            with patch ( 'googlepostmasterapi.data.FlatData._parse_use_auth' ) as parse_use_auth:
                                with patch ( 'googlepostmasterapi.data.FlatData._parse_crypted_inbound' ) as parse_crypted_inbound:
                                    with patch ( 'googlepostmasterapi.data.FlatData._parse_delivery_err' ) as parse_delivery_err:
                                        deepcopy.return_value = 'random-dict';
                                        index_domain_stats.return_value = {
                                            'spam_rate': 'random-spam-rate',
                                            'auth_dkim': 'random-auth-dkim',
                                            'auth_spf': 'random-auth-spf',
                                            'auth_dmarc': 'random-auth-dmarc',
                                            'tls_inbound': 'random-tls-inbound',
                                            'feedback_loop_id': 'random-feedback-loop-id-value',
                                            'feedback_loop_spam_rate__123': 'random-fbl-123',
                                            'feedback_loop_spam_rate__456': 'random-fbl-456',
                                            'delivery_error__reject__bad_attachment': 'random-de-1',
                                            'delivery_error__temp_fail__other': 'random-de-2',
                                            'other_metric': 'random-other'
                                        };

                                        f = FlatData ();
                                        f._data_tpl = { 'random-key': 'random-value' };

                                        ret = f.parse (
                                            key = 'random-key',
                                            data = {
                                                'domainStats': 'random-domain-stats',
                                                'complianceStatus': {
                                                    'complianceData': 'random-compliance-data'
                                                }
                                            }
                                        );

                                        self.assertEqual ( ret, 'random-dict' );
                                        self.assertEqual ( 'random-key' in f.data, False );
                                        
                                        self.assertEqual ( deepcopy.call_count, 2 );
                                        deepcopy.assert_any_call ( { 'random-key': 'random-value' } );
                                        deepcopy.assert_any_call ( 'random-dict' );
                                        index_domain_stats.assert_called_once_with (
                                            domain_stats = 'random-domain-stats'
                                        );
                                        parse_user_report_spam.assert_called_with (
                                            key = 'random-key',
                                            value = 'random-spam-rate'
                                        );
                                        parse_domain_compliance.assert_called_with (
                                            key = 'random-key',
                                            value = 'random-compliance-data'
                                        );
                                        parse_fbl.assert_called_with (
                                            key = 'random-key',
                                            value = {
                                                '123': 'random-fbl-123',
                                                '456': 'random-fbl-456'
                                            }
                                        );
                                        parse_use_auth.assert_called_with (
                                            key = 'random-key',
                                            dkim = 'random-auth-dkim',
                                            spf = 'random-auth-spf',
                                            dmarc = 'random-auth-dmarc'
                                        );
                                        parse_crypted_inbound.assert_called_with (
                                            key = 'random-key',
                                            value = 'random-tls-inbound'
                                        );
                                        parse_delivery_err.assert_called_with (
                                            key = 'random-key',
                                            value = {
                                                'reject__bad_attachment': 'random-de-1',
                                                'temp_fail__other': 'random-de-2'
                                            }
                                        );


    def test_no_domain_stats_or_compliance ( self ):
        with patch ( 'googlepostmasterapi.data.copy.deepcopy' ) as deepcopy:
            with patch ( 'googlepostmasterapi.data.FlatData._index_domain_stats' ) as index_domain_stats:
                with patch ( 'googlepostmasterapi.data.FlatData._parse_user_report_spam' ) as parse_user_report_spam:
                    with patch ( 'googlepostmasterapi.data.FlatData._parse_domain_compliance' ) as parse_domain_compliance:
                        with patch ( 'googlepostmasterapi.data.FlatData._parse_fbl' ) as parse_fbl:
                            with patch ( 'googlepostmasterapi.data.FlatData._parse_use_auth' ) as parse_use_auth:
                                with patch ( 'googlepostmasterapi.data.FlatData._parse_crypted_inbound' ) as parse_crypted_inbound:
                                    with patch ( 'googlepostmasterapi.data.FlatData._parse_delivery_err' ) as parse_delivery_err:
                                        deepcopy.return_value = 'random-dict';
                                        index_domain_stats.return_value = {};

                                        f = FlatData ();
                                        f._data_tpl = { 'random-key': 'random-value' };

                                        ret = f.parse (
                                            key = 'random-key',
                                            data = {}
                                        );

                                        self.assertEqual ( ret, 'random-dict' );
                                        index_domain_stats.assert_called_once_with (
                                            domain_stats = []
                                        );
                                        parse_domain_compliance.assert_called_with (
                                            key = 'random-key',
                                            value = None
                                        );
                                        parse_fbl.assert_called_with (
                                            key = 'random-key',
                                            value = {}
                                        );
                                        parse_delivery_err.assert_called_with (
                                            key = 'random-key',
                                            value = {}
                                        );


if __name__ == '__main__':
    unittest.main ();
