#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os;
import unittest;

from pprint import pprint;
from unittest.mock import patch, Mock;


from googlepostmasterapi.gpt import GPostmaster;


@patch ( 'googlepostmasterapi.gpt.GPostmaster._init_resources', Mock ( return_value = None ) )
class GPostmaster_create_domainTest ( unittest.TestCase ):
    def test_calls ( self ):
        with patch ( 'googlepostmasterapi.gpt.GPostmaster._gpt_create_domain' ) as gpt_create_domain:
            with patch ( 'googlepostmasterapi.gpt.GPostmaster.get_domain_verify_token' ) as get_domain_verify_token:
                gpt_create_domain.return_value = True;
                get_domain_verify_token.return_value = 'random-token-value';

                g = GPostmaster (
                    token = 'random-token'
                );

                ret = g.create_domain (
                    domain = 'random-domain'
                );

                self.assertEqual ( ret, {
                    'state': True,
                    'token': 'random-token-value'
                } );
                
                gpt_create_domain.assert_called_once_with (
                    domain = 'random-domain'
                );
                get_domain_verify_token.assert_called_once_with (
                    domain = 'random-domain'
                );


    def test_creation_failed ( self ):
        with patch ( 'googlepostmasterapi.gpt.GPostmaster._gpt_create_domain' ) as gpt_create_domain:
            with patch ( 'googlepostmasterapi.gpt.GPostmaster.get_domain_verify_token' ) as get_domain_verify_token:
                gpt_create_domain.return_value = False;

                g = GPostmaster (
                    token = 'random-token'
                );

                ret = g.create_domain (
                    domain = 'random-domain'
                );

                self.assertEqual ( ret, {
                    'state': False
                } );
                
                gpt_create_domain.assert_called_once_with (
                    domain = 'random-domain'
                );
                get_domain_verify_token.assert_not_called ();


if __name__ == '__main__':
    unittest.main ();
