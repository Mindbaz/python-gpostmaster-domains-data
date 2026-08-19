#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.gpt import GPostmaster;


@patch ( 'googlepostmasterapi.base.Base.__init__', Mock ( return_value = None ) )
@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster_verify_domainTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.gpt.GPostmaster._gpt_verify_domain' ) as gpt_verify_domain:
            gpt_verify_domain.return_value = 'random-returns';

            g = GPostmaster (
                token = 'random-token'
            );

            ret = g.verify_domain (
                domain = 'random-domain'
            );

            self.assertEqual ( ret, 'random-returns' );
            
            gpt_verify_domain.assert_called_once_with (
                domain = 'random-domain'
            );



if __name__ == '__main__':
    unittest.main ();
