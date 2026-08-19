#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.gpt import GPostmaster;


@patch ( 'googlepostmasterapi.base.Base.__init__', Mock ( return_value = None ) )
@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster_get_domain_infosTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.gpt.GPostmaster._gpt_get_domain_info' ) as gpt_get_domain_info:
            with patch ( 'googlepostmasterapi.gpt.GPostmaster._clean_domain_infos' ) as clean_domain_infos:
                with patch ( 'googlepostmasterapi.gpt.GPostmaster._print_stats' ) as print_stats:
                    gpt_get_domain_info.return_value = {
                        'state': True,
                        'result': 'random-domain-info'
                    };
                    clean_domain_infos.return_value = {
                        'random-key': 'random-data-cleaned'
                    };
                    
                    g = GPostmaster (
                        token = 'random-token'
                    );
                    
                    ret = g.get_domain_infos (
                        domain = 'random-domain',
                        input_date = 'random-input-date'
                    );
                    
                    self.assertEqual ( ret [ 'state' ], True );
                    self.assertEqual ( ret [ 'result' ], { 'random-key': 'random-data-cleaned', 'domain': 'random-domain', 'date': 'random-input-date' } );
                    self.assertEqual ( ret [ 'domain' ], 'random-domain' );
                    self.assertEqual ( ret [ 'date' ], 'random-input-date' );
                    gpt_get_domain_info.assert_called_with (
                        domain = 'random-domain',
                        input_date = 'random-input-date'
                    );
                    clean_domain_infos.assert_called_with (
                        key = 'random-domain-random-input-date',
                        data = 'random-domain-info'
                    );
                    print_stats.assert_called_once_with ();

                        
    def test_gpt_get_domain_info_return_false ( self ):
        with patch ( 'googlepostmasterapi.gpt.GPostmaster._gpt_get_domain_info' ) as gpt_get_domain_info:
            with patch ( 'googlepostmasterapi.gpt.GPostmaster._clean_domain_infos' ) as clean_domain_infos:
                with patch ( 'googlepostmasterapi.gpt.GPostmaster._print_stats' ) as print_stats:
                    gpt_get_domain_info.return_value = {
                        'state': False
                    };
                    clean_domain_infos.return_value = 'random-data-cleaned';
                    
                    g = GPostmaster (
                        token = 'random-token'
                    );
                    
                    ret = g.get_domain_infos (
                        domain = 'random-domain',
                        input_date = 'random-input-date'
                    );
                    
                    self.assertEqual ( ret [ 'state' ], False );
                    self.assertEqual ( ret [ 'domain' ], 'random-domain' );
                    self.assertEqual ( ret [ 'date' ], 'random-input-date' );
                    
                    gpt_get_domain_info.assert_called_with (
                        domain = 'random-domain',
                        input_date = 'random-input-date'
                    );
                    clean_domain_infos.assert_not_called ();
                    print_stats.assert_called_once_with ();
                    
                    
    def test_do_not_print_sats ( self ):
        with patch ( 'googlepostmasterapi.gpt.GPostmaster._gpt_get_domain_info' ) as gpt_get_domain_info:
            with patch ( 'googlepostmasterapi.gpt.GPostmaster._clean_domain_infos' ) as clean_domain_infos:
                with patch ( 'googlepostmasterapi.gpt.GPostmaster._print_stats' ) as print_stats:
                    gpt_get_domain_info.return_value = {
                        'state': True,
                        'result': 'random-domain-info'
                    };
                    clean_domain_infos.return_value = {
                        'random-key': 'random-data-cleaned'
                    };
                    
                    g = GPostmaster (
                        token = 'random-token'
                    );
                    
                    ret = g.get_domain_infos (
                        domain = 'random-domain',
                        input_date = 'random-input-date',
                        print_stats = False
                    );
                    
                    self.assertEqual ( ret [ 'state' ], True );
                    self.assertEqual ( ret [ 'result' ], { 'random-key': 'random-data-cleaned', 'domain': 'random-domain', 'date': 'random-input-date' } );
                    self.assertEqual ( ret [ 'domain' ], 'random-domain' );
                    self.assertEqual ( ret [ 'date' ], 'random-input-date' );
                    gpt_get_domain_info.assert_called_with (
                        domain = 'random-domain',
                        input_date = 'random-input-date'
                    );
                    clean_domain_infos.assert_called_with (
                        key = 'random-domain-random-input-date',
                        data = 'random-domain-info'
                    );
                    print_stats.assert_not_called ();
                    
            
if __name__ == '__main__':
    unittest.main ();
