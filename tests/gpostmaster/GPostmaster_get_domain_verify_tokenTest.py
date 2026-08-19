#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.gpt import GPostmaster;


@patch ( 'googlepostmasterapi.base.Base.__init__', Mock ( return_value = None ) )
@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster_get_domain_verify_tokenTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.gpt.GPostmaster._gpt_get_domain_verify_token' ) as gpt_get_domain_verify_token:
            gpt_get_domain_verify_token.return_value = 'random-token-value';

            g = GPostmaster (
                token = 'random-token'
            );

            ret = g.get_domain_verify_token (
                domain = 'random-domain'
            );

            self.assertEqual ( ret, 'random-token-value' );
            
            gpt_get_domain_verify_token.assert_called_once_with (
                domain = 'random-domain'
            );


if __name__ == '__main__':
    unittest.main ();
