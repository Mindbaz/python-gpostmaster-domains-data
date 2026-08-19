#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.gpt import GPostmaster;
from googleapiclient.errors import HttpError;


@patch ( 'googlepostmasterapi.base.Base.__init__', Mock ( return_value = None ) )
@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster__create_pool_dataTest ( unittest.TestCase ):
    def test_calls ( self ):
        g = GPostmaster (
            token = 'random-token'
        );
        g._domains = [ 'random-domain-1', 'random-domain-2', 'random-domain-3' ];
        
        ret = g._create_pool_data (
            input_date = 'random-input-date'
        );
        self.assertEqual ( ret, [
            { 'domain': 'random-domain-1', 'input_date': 'random-input-date' },
            { 'domain': 'random-domain-2', 'input_date': 'random-input-date' },
            { 'domain': 'random-domain-3', 'input_date': 'random-input-date' }
        ] );
            
            
if __name__ == '__main__':
    unittest.main ();
