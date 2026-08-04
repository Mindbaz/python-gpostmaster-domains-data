#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googleapiclient.errors import HttpError;
from googlepostmasterapi.gpt import GPostmaster;


@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster__get_domain_infos_poolTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.gpt.GPostmaster.get_domain_infos' ) as get_domain_infos:
            get_domain_infos.return_value = 'random-returns';
            
            g = GPostmaster (
                token = 'random-token'
            );
            
            ret = g._get_domain_infos_pool (
                data = {
                    'domain': 'random-domain',
                    'input_date': 'random-input-date'
                } );
            self.assertEqual ( ret, 'random-returns' );
            get_domain_infos.assert_called_with (
                domain = 'random-domain',
                input_date = 'random-input-date',
                print_stats = False
            );
            
            
if __name__ == '__main__':
    unittest.main ();
