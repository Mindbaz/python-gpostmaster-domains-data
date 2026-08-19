#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googleapiclient.errors import HttpError;
from googlepostmasterapi.gpt import GPostmaster;


@patch ( 'googlepostmasterapi.base.Base.__init__', Mock ( return_value = None ) )
@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster__clean_pool_returnsTest ( unittest.TestCase ):
    def test_calls ( self ):
        g = GPostmaster (
            token = 'random-token'
        );
        
        ret = g._clean_pool_returns (
            data = [
                { 'state': False, 'key': 'random-data-1' },
                { 'state': True, 'key': 'random-data-2' },
                { 'state': False, 'key': 'random-data-3' },
                { 'state': True, 'key': 'random-data-4' }
            ] );
        self.assertEqual ( ret, [
            { 'state': True, 'key': 'random-data-2' },
            { 'state': True, 'key': 'random-data-4' }
        ] );
            
            
if __name__ == '__main__':
    unittest.main ();
