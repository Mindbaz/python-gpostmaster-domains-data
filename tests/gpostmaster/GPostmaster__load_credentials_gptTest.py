#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.gpt import GPostmaster;


@patch ( 'googlepostmasterapi.base.Base.__init__', Mock ( return_value = None ) )
@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster__load_tokenTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.gpt.Credentials.from_authorized_user_file' ) as from_authorized_user_file:
            from_authorized_user_file.return_value = 'random-returns';
            
            g = GPostmaster (
                token = 'random-token'
            );
            g.scopes = 'random-scopes';
            
            ret = g._load_token (
                token = 'another-token'
            );
            
            self.assertEqual ( ret, 'random-returns' );

            from_authorized_user_file.assert_called_once_with (
                'another-token',
                'random-scopes'
            );

            
if __name__ == '__main__':
    unittest.main ();
